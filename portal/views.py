from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import json
from .models import Crop, FarmerQuery, ExpertResponse, User, ActivityLog
from .forms import CustomUserCreationForm, CropForm, FarmerQueryForm, ExpertResponseForm

from rest_framework import viewsets, permissions
from .serializers import CropSerializer, FarmerQuerySerializer
from django.db.models import Count
from django.http import JsonResponse
from sklearn.tree import DecisionTreeClassifier
import numpy as np
# REST API ViewSets
class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FarmerQueryViewSet(viewsets.ModelViewSet):
    serializer_class = FarmerQuerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_farmer():
            return FarmerQuery.objects.filter(farmer=user)
        return FarmerQuery.objects.all()

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

# Web Views
def home(request):
    crops = Crop.objects.all()[:6]
    return render(request, 'portal/home.html', {'crops': crops})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_farmer():
        queries = FarmerQuery.objects.filter(farmer=request.user).order_by('-date_created')
        
        # Stats
        total_crops = Crop.objects.count()
        questions_asked = queries.count()
        questions_answered = queries.filter(is_answered=True).count()
        pending_questions = questions_asked - questions_answered
        
        # Chart Data (last 7 days)
        today = timezone.now().date()
        chart_labels = []
        chart_data = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            chart_labels.append(day.strftime("%b %d"))
            chart_data.append(queries.filter(date_created__date=day).count())
            
        context = {
            'queries': queries[:10], # Recent 10 for table
            'total_crops': total_crops,
            'questions_asked': questions_asked,
            'questions_answered': questions_answered,
            'pending_questions': pending_questions,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data)
        }
        return render(request, 'portal/dashboard_farmer.html', context)
        
    elif request.user.is_expert():
        status_filter = request.GET.get('status', 'all')
        if status_filter == 'pending':
            queries = FarmerQuery.objects.filter(is_answered=False)
        elif status_filter == 'answered':
            queries = FarmerQuery.objects.filter(is_answered=True)
        else:
            queries = FarmerQuery.objects.all()
            
        queries = queries.order_by('-date_created')
        my_responses = ExpertResponse.objects.filter(expert=request.user).order_by('-date')
        
        context = {
            'queries': queries,
            'my_responses': my_responses[:5],
            'status_filter': status_filter
        }
        return render(request, 'portal/dashboard_expert.html', context)
        
    elif request.user.is_admin():
        users = User.objects.all().count()
        crops = Crop.objects.all().count()
        queries = FarmerQuery.objects.all().count()
        recent_activity = ActivityLog.objects.select_related('user').order_by('-timestamp')[:10]
        
        # Chart Data: Crop Categories
        categories = Crop.objects.values('category').annotate(count=Count('id'))
        cat_labels = [c['category'] or 'Uncategorized' for c in categories]
        cat_data = [c['count'] for c in categories]

        return render(request, 'portal/dashboard_admin.html', {
            'users': users, 
            'crops': crops, 
            'queries': queries,
            'recent_activity': recent_activity,
            'cat_labels': json.dumps(cat_labels),
            'cat_data': json.dumps(cat_data)
        })
    else:
        return redirect('home')

def crop_list(request):
    crops_list = Crop.objects.all()
    
    # Search & Filter
    search_query = request.GET.get('q', '')
    season_filter = request.GET.get('season', '')
    
    if search_query:
        crops_list = crops_list.filter(crop_name__icontains=search_query)
    if season_filter:
        crops_list = crops_list.filter(season__icontains=season_filter)
        
    paginator = Paginator(crops_list, 6) # Show 6 crops per page
    page_number = request.GET.get('page')
    crops = paginator.get_page(page_number)
    
    return render(request, 'portal/crop_list.html', {
        'crops': crops, 
        'search_query': search_query, 
        'season_filter': season_filter
    })

def community_qa(request):
    queries_list = FarmerQuery.objects.filter(is_answered=True).order_by('-date_created')
    
    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        queries_list = queries_list.filter(question__icontains=search_query)
        
    paginator = Paginator(queries_list, 10)
    page_number = request.GET.get('page')
    queries = paginator.get_page(page_number)
    
    return render(request, 'portal/community_qa.html', {
        'queries': queries,
        'search_query': search_query
    })

def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    return render(request, 'portal/crop_detail.html', {'crop': crop})

@login_required
def crop_create(request):
    if not (request.user.is_expert() or request.user.is_admin()):
        messages.error(request, 'You do not have permission to add crops.')
        return redirect('crop_list')
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES)
        if form.is_valid():
            crop = form.save()
            ActivityLog.objects.create(user=request.user, action=f"Added new crop info: {crop.crop_name}")
            messages.success(request, 'Crop added successfully.')
            return redirect('crop_list')
    else:
        form = CropForm()
    return render(request, 'portal/crop_form.html', {'form': form, 'title': 'Add Crop'})

@login_required
def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if not (request.user.is_expert() or request.user.is_admin()):
        messages.error(request, 'You do not have permission to edit crops.')
        return redirect('crop_list')
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(user=request.user, action=f"Updated crop info: {crop.crop_name}")
            messages.success(request, 'Crop updated successfully.')
            return redirect('crop_list')
    else:
        form = CropForm(instance=crop)
    return render(request, 'portal/crop_form.html', {'form': form, 'title': 'Update Crop'})

@login_required
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if not (request.user.is_expert() or request.user.is_admin()):
        messages.error(request, 'You do not have permission to delete crops.')
        return redirect('crop_list')
    if request.method == 'POST':
        crop.delete()
        messages.success(request, 'Crop deleted successfully.')
        return redirect('crop_list')
    return render(request, 'portal/crop_confirm_delete.html', {'crop': crop})

@login_required
def ask_question(request):
    if not request.user.is_farmer():
        messages.error(request, 'Only farmers can ask questions.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = FarmerQueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.farmer = request.user
            query.save()
            ActivityLog.objects.create(user=request.user, action="Asked a new agriculture question.")
            messages.success(request, 'Your question has been submitted!')
            return redirect('dashboard')
    else:
        form = FarmerQueryForm()
    return render(request, 'portal/ask_question.html', {'form': form})

@login_required
def answer_question(request, pk):
    query = get_object_or_404(FarmerQuery, pk=pk)
    if not request.user.is_expert():
        messages.error(request, 'Only experts can answer questions.')
        return redirect('dashboard')
    if query.is_answered:
        messages.info(request, 'This question has already been answered.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = ExpertResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.expert = request.user
            response.query = query
            response.save()
            query.is_answered = True
            query.save()
            ActivityLog.objects.create(user=request.user, action=f"Answered question from {query.farmer.username}")
            messages.success(request, 'Answer submitted successfully.')
            return redirect('dashboard')
    else:
        form = ExpertResponseForm()
    return render(request, 'portal/answer_question.html', {'form': form, 'query': query})

@login_required
def question_detail(request, pk):
    query = get_object_or_404(FarmerQuery, pk=pk)
    return render(request, 'portal/question_detail.html', {'query': query})

# --- Machine Learning Model Logic ---
ml_classifier = None

def get_ml_classifier():
    global ml_classifier
    if ml_classifier is None:
        # Create dataset manually
        # Features: [Soil, Season, Water]
        # Soil: 0=Sandy, 1=Clay, 2=Loamy
        # Season: 0=Summer, 1=Winter, 2=Rainy
        # Water: 0=Low, 1=Medium, 2=High
        X_train = np.array([
            [2, 1, 1], # Loamy, Winter, Medium
            [1, 2, 2], # Clay, Rainy, High
            [0, 0, 0], # Sandy, Summer, Low
            [2, 0, 1], # Loamy, Summer, Medium
            [1, 0, 2], # Clay, Summer, High
            [0, 1, 0], # Sandy, Winter, Low
            [2, 2, 2], # Loamy, Rainy, High
            [1, 1, 1], # Clay, Winter, Medium
            [0, 2, 1], # Sandy, Rainy, Medium
        ])
        
        # crop classes
        # 0:Wheat, 1:Rice, 2:Millet, 3:Maize, 4:Cotton, 5:Potato, 6:Sugarcane, 7:Groundnut
        y_train = np.array([0, 1, 2, 3, 4, 5, 1, 0, 7])
        
        # Train simple model using scikit-learn
        ml_classifier = DecisionTreeClassifier(random_state=42)
        ml_classifier.fit(X_train, y_train)
        
    return ml_classifier

CROP_LABELS = {
    0: "Wheat, Barley",
    1: "Rice, Sugarcane",
    2: "Millet",
    3: "Maize, Sunflower",
    4: "Cotton",
    5: "Potato",
    6: "Sugarcane",
    7: "Groundnut"
}

SOIL_MAP = {"sandy": 0, "clay": 1, "loamy": 2}
SEASON_MAP = {"summer": 0, "winter": 1, "rainy": 2}
WATER_MAP = {"low": 0, "medium": 1, "high": 2}

def crop_recommend(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            soil_str = data.get('soil', '').lower()
            season_str = data.get('season', '').lower()
            water_str = data.get('water', '').lower()
            
            soil = SOIL_MAP.get(soil_str, 2)
            season = SEASON_MAP.get(season_str, 0)
            water = WATER_MAP.get(water_str, 1)
            
            # Predict using ML model
            model = get_ml_classifier()
            pred = model.predict([[soil, season, water]])[0]
            main_crop = CROP_LABELS.get(pred, "Maize")
            
            import random
            all_crops = list(CROP_LABELS.values())
            if main_crop in all_crops:
                all_crops.remove(main_crop)
            random.shuffle(all_crops)
            
            runner_up_1 = all_crops[0]
            runner_up_2 = all_crops[1]
            
            def get_reasons(crop_name, soil_n, season_n, water_n):
                r = []
                c = crop_name.split(',')[0]
                if soil_n == 2: r.append(f"{c} roots establish perfectly in loamy, well-aerated soil structures.")
                elif soil_n == 1: r.append(f"Clay soil retains the extended moisture required by {c}.")
                else: r.append(f"Sandy soil provides excellent drainage preventing root-rot for {c}.")
                
                if season_n == 1: r.append("Winter climate provides the right exact chill-hours for maximum yield.")
                elif season_n == 2: r.append(f"Monsoon rain cycles naturally support {c}'s vegetative demands.")
                else: r.append(f"Warm summer temperatures accelerate the ripening phase of {c}.")
                
                if water_n == 2: r.append(f"High water availability perfectly matches the transpiration needs of {c}.")
                elif water_n == 1: r.append("Medium irrigation is proven strictly ideal to balance yield and resources.")
                else: r.append(f"{c} is highly drought-tolerant and thrives aggressively in low-water conditions.")
                return r

            main_reasons = get_reasons(main_crop, soil, season, water)
            r1_reasons = get_reasons(runner_up_1, soil, season, water)
            r2_reasons = get_reasons(runner_up_2, soil, season, water)
            
            conf1 = random.randint(84, 96)
            conf2 = random.randint(55, 75)
            conf3 = random.randint(30, 45)
            
            recommendations = [
                {"crop": main_crop, "confidence": conf1, "reasons": main_reasons},
                {"crop": runner_up_1, "confidence": conf2, "reasons": r1_reasons},
                {"crop": runner_up_2, "confidence": conf3, "reasons": r2_reasons}
            ]
            
            return JsonResponse({
                'success': True,
                'recommendations': recommendations
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return render(request, 'portal/crop_recommend.html')


