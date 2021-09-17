from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from WebApp.forms import *
from WebApp.models import *
from datetime import date
import WebApp.extract_text
import os
import fitz
import json

# Create your views here.

def login_required_check(view):
    def updated_view(request):
        try:
            if request.session["loged_in"] == True:
                return view(request)
            else:
                return redirect(login)
        except KeyError:
            return redirect(login)
    return updated_view

def not_loged_in_check(view):
    def updated_view(request):
        try:
            if request.session["loged_in"] == False:
                return view(request)
            else:
                return redirect(homepage)
        except:
            return view(request)
    
    return updated_view

def create_cookies(view):
    def updated_view(request):
        try:
            if request.session['loged_in'] == False:
                temp = True
        except:
            request.session['loged_in'] = False
            pass
        
        try:
            if request.session['username'] == False:
                temp = True
        except:
            request.session['username'] = None
            pass

        try:
            if request.session['name'] == False:
                temp = True
        except:
            request.session['name'] = None
            pass

        try:
            if request.session['chosen_file'] == False:
                temp = True
        except:
            request.session['chosen_file'] = None
            pass
        return view(request)
    return updated_view



@create_cookies
def login(request):
    request.session['chosen_file'] = None
    errorMessage = ''
    if request.method == 'POST':
        user_input = loginForms(request.POST)
        if user_input.is_valid():
            entered_username = user_input.cleaned_data["username"]
            entered_password = user_input.cleaned_data["password"]
            if Users.objects.filter(username=entered_username):
                if Users.objects.filter(username=entered_username).filter(password=entered_password):
                    request.session['username'] = entered_username
                    request.session['loged_in'] = True
                    request.session['name'] = Users.objects.get(username=entered_username).name
                    return redirect(homepage)
                else:
                    request.session['loged_in'] = False
                    errorMessage = 'Wrong password'
            else:
                request.session['loged_in'] = False
                errorMessage = 'No such account'

    return render(request, "WebApp/login.html", {
        'name': None,
        'loginForm': loginForms(),
        'errorMessage': errorMessage,
        'loged_in': request.session['loged_in']
    })

@login_required_check
def upload(request):
    request.session['chosen_file'] = None
    errorMessage = ''
    if request.method == 'POST':
        uploaded_document = request.FILES['document']
        resource = Resource(
            uploaded_by = Users.objects.get(username=request.session['username']),
            upload_date = date.today(),
            resource_name = uploaded_document.name,
            raw_resource = uploaded_document
        )
        resource.save()

        user_files = Resource.objects.filter(uploaded_by=Users.objects.get(username=request.session['username']))
        total_size = 0
        for file in user_files:
            total_size += os.stat(file.raw_resource.path).st_size / (1024 * 1024)
        if total_size > 50:
            file = Resource.objects.filter(uploaded_by=Users.objects.get(username=request.session['username'])).get(resource_name=uploaded_document.name)
            to_delete_size = os.stat(file.raw_resource.path).st_size / (1024 * 1024)
            total_size -= to_delete_size
            filepath = file.raw_resource.path
            file.delete()
            try:
                os.remove(filepath)
            except:
                pass
            errorMessage = f'The size of your combined files exceded 50 Mb. Your combined file size is currently {total_size} Mb'
        
    return render(request, 'WebApp/upload.html', {
        'name': None,
        'form': uploadResourceForms,
        'name': request.session["name"],
        'errorMessage': errorMessage,
        'loged_in': request.session['loged_in']
    })

@create_cookies
@not_loged_in_check
def signup(request):
    errorMessage = ''
    if request.method == 'POST':
        user_input = signUpForms(request.POST)
        try:
            if user_input.is_valid():
                user = Users(
                    name=user_input.cleaned_data["name"],
                    username=user_input.cleaned_data["username"],
                    password=user_input.cleaned_data["password"],
                    email=user_input.cleaned_data["email"],
                    reason_for_use=user_input.cleaned_data["reason_for_use"],
                    user_type=user_input.cleaned_data["user_type"]
                )
                user.save()
                request.session['name'] = user_input.cleaned_data["name"]
                request.session['username'] = user_input.cleaned_data["username"]
                request.session['loged_in'] = True
                return redirect(homepage)
        except:
            errorMessage = 'Username is taken'
            pass


    return render(request, "WebApp/signup.html", {
        'name': None,
        'DisplayForm': signUpForms(),
        'errorMessage': errorMessage,
        'loged_in': request.session['loged_in']
    })

@create_cookies
def homepage(request):
    request.session['chosen_file'] = None
    return render(request, "WebApp/homepage.html", {
        'name': request.session["name"],
        'loged_in': request.session['loged_in']
    })

@login_required_check
def logout(request):
    request.session['chosen_file'] = None
    if request.method == 'POST':
        request.session['username'] = None
        request.session['loged_in'] = False
        return redirect(login)
    else:
        return render(request, "WebApp/logout.html", {
            'name': request.session["name"],
            'loged_in': request.session['loged_in']
        })

@login_required_check
def choosefile(request):
    if request.method == 'POST':
        request.session["chosen_file"] = Resource.objects.get(id=request.POST['button']).raw_resource.path
    
        request.session["chosen_file_name"] = Resource.objects.get(id=request.POST['button']).resource_name
        return redirect(askquestion)
    else:
        resources = Resource.objects.filter(uploaded_by=Users.objects.get(username=request.session["username"]))
        ELE_PER_ROW = 4

        main_counter = 1
        split_resource_list = {}
        temp = []
        counter = 1
        for resource in resources:
            if counter > 4:
                split_resource_list[str(main_counter)] = temp
                main_counter += 1
                counter = 2
                temp = []
                temp.append(resource)
            else:
                temp.append(resource)
                counter += 1
            
        while len(temp) != ELE_PER_ROW:
            temp.append(None)
        split_resource_list[str(main_counter)] = temp

        return render(request, "WebApp/choosefile.html", {
            'resources': split_resource_list,
            'name': request.session["name"],
            'loged_in': request.session['loged_in']
        })

@login_required_check
def delete(request):
    request.session["chosen_file"] = None
    if request.method == 'POST':
        file = Resource.objects.get(id=request.POST['button'])
        filepath = file.raw_resource.path
        file.delete()
        try:
            os.remove(filepath)
        except:
            pass

    resources = Resource.objects.filter(uploaded_by=Users.objects.get(username=request.session["username"]))
    ELE_PER_ROW = 4

    main_counter = 1
    split_resource_list = {}
    temp = []
    counter = 1
    for resource in resources:
        if counter > 4:
            split_resource_list[str(main_counter)] = temp
            main_counter += 1
            counter = 2
            temp = []
            temp.append(resource)
        else:
            temp.append(resource)
            counter += 1
        
    while len(temp) != ELE_PER_ROW:
        temp.append(None)
    split_resource_list[str(main_counter)] = temp


    return render(request, "WebApp/delete.html", {
        'resources': split_resource_list,
        'name': request.session["name"],
        'loged_in': request.session['loged_in']
    })

def help(request):
    request.session['chosen_file'] = None
    return render(request, "WebApp/help.html", {
        'name': request.session["name"],
        'loged_in': request.session['loged_in']
    })

@not_loged_in_check
def terms(request):
    return render(request, "WebApp/termsandconditions.html")



@login_required_check
def askquestion(request):

    def highlight_and_show(match, page_relation, type="paragraph"):
        CHOSEN_FILE = 'media/temp_files/' + request.session["username"] + '_temp.pdf'

        try:
            for page_num in range(1, len(page_relation)):
                if match in page_relation[str(page_num)]:
                    break
        except:
            for page_num in range(1, len(page_relation)):
                if match in page_relation[page_num]:
                    break

        CHOSEN_FILE += '#page=' + str(page_num)

        doc = fitz.open(request.session['chosen_file'])
        page = doc[page_num - 1]
        if type == 'paragraph':
            match = match.split('.')
            text_instances = page.searchFor(match[0])
            for m in match[1:]:
                if m != ' ' and m != '':
                    try:
                        text_instances.append(page.searchFor(m))
                    except:
                        pass
        else:
            match = match.split('.')
            match.append('')
            try:
                text_instances = page.searchFor(match[0])
            except:
                text_instances = list()
            if text_instances is None:
                text_instances = list()
            for m in match[1:]:
                if m != ' ':
                    text_instances.append(page.searchFor(m))

        ### HIGHLIGHT
        for inst in text_instances:
            highlight = page.addHighlightAnnot(inst)
            highlight.update()


        ### OUTPUT
        try:
            os.remove('/media/temp_files/' + request.session["username"] + '_temp.pdf')
        except:
            pass
        doc.save('media/temp_files/' + request.session["username"] + '_temp.pdf', garbage=4, deflate=True, clean=True)

        return CHOSEN_FILE


    if request.session["chosen_file"] != None:
        BERT_ANSWER = ''
        CHOSEN_FILE = '/media/resources/' + request.session['chosen_file'].split('\\')[-1]
        SHOW_1 = True
        SHOW_2 = False
        SHOW_2_BACK = False
        SHOW_3 = False
        SHOW_3_BACK = False
        SHOW_4 = False
        SHOW_ANSWER = False
        SHOW_ERROR = False


        if request.method == "POST":
            if request.is_ajax():
                if request.POST["tag"] == "Submit":
                    request.session["query"] = request.POST["query"]
                    request.session["matches"] = json.loads(request.POST['sentences'])
                    request.session["match_pos"] = 0

                    match = request.session["matches"][request.session["match_pos"]]
                    request.session["CHOSEN_FILE"] = highlight_and_show(match, request.session['page_relation'], type="page")
                    request.session["SHOW_2"] = True
                    request.session["SHOW_3"] = False
                    request.session["SHOW_4"] = False
                    request.session["SHOW_ANSWER"] = False
                    request.session["question_variables_stored_in_session"] = True
                    request.session["session_variable_limit"] = 1
            

                if request.POST["tag"] == "Correct Page":
                    match = request.session["matches"][request.session["match_pos"]]
                    request.session["chosen_page"] = match.replace('.', '.\n\n')
                    request.session["sentence_matches"] = json.loads(request.POST["sentences"])
                    request.session["paragraph_matches"] = json.loads(request.POST["paragraphs"])
                    request.session["sentence_pos"] = 0
                    request.session["paragraph"] = request.session["paragraph_matches"][request.session["sentence_pos"]]
                    
                    request.session["CHOSEN_FILE"] = highlight_and_show(request.session["paragraph"].replace('.\n\n', '.'), request.session["page_relation"])
                    request.session["SHOW_2"] = False
                    request.session["SHOW_3"] = True
                    request.session["SHOW_4"] = False
                    request.session["SHOW_ANSWER"] = False
                    request.session["question_variables_stored_in_session"] = True
                    request.session["session_variable_limit"] = 1


                if request.POST["tag"] == "Answer":
                    request.session["all_bert_answers"] = json.loads(request.POST["answers"])
                    request.session["bert_answer_pos"] = 0
                    request.session["BERT_ANSWER"] = request.session["all_bert_answers"][request.session["bert_answer_pos"]]["text"]
                    request.session["SHOW_2"] = False
                    request.session["SHOW_3"] = False
                    request.session["SHOW_4"] = True
                    request.session["SHOW_ANSWER"] = True
                    request.session["question_variables_stored_in_session"] = True
                    request.session["session_variable_limit"] = 1


            else:
                if request.POST["button"] == "incorrect_page":
                    request.session["match_pos"] += 1
                    if request.session["match_pos"] > len(request.session['matches']) - 1:
                        SHOW_2 = False
                        SHOW_ERROR = True
                        CHOSEN_FILE = request.session["chosen_file"]
                    else:
                        match = request.session["matches"][request.session["match_pos"]]
                        SHOW_2 = True
                        CHOSEN_FILE = highlight_and_show(match, request.session['page_relation'], type="page")

                    if request.session["match_pos"] != 0:
                        SHOW_2_BACK = True
                        CHOSEN_FILE = highlight_and_show(match, request.session['page_relation'], type="page")


                if request.POST["button"] == "go_back":
                    request.session["match_pos"] -= 1
                    match = request.session["matches"][request.session["match_pos"]]

                    CHOSEN_FILE = highlight_and_show(match, request.session['page_relation'], type="page")
                    SHOW_2 = True

                    if request.session["match_pos"] != 0:
                        SHOW_2_BACK = True
                    

                if request.POST["button"] == 'incorrect_paragraph':
                    if request.session["sentence_pos"] == len(request.session['sentence_matches']) - 1:
                        SHOW_3 = False
                        SHOW_ERROR = True
                        CHOSEN_FILE = request.session["chosen_file"]
                    else:
                        request.session["sentence_pos"] += 1
                        request.session["paragraph"] = request.session["paragraph_matches"][request.session["sentence_pos"]]
                        SHOW_3 = True
                        CHOSEN_FILE = highlight_and_show(request.session["paragraph"], request.session["page_relation"])

                    if request.session["sentence_pos"] != 0:
                        SHOW_3_BACK = True
                        CHOSEN_FILE = highlight_and_show(request.session["paragraph"], request.session["page_relation"])

                
                if request.POST["button"] == 'go_back_paragraph':
                    request.session["sentence_pos"] -= 1
                    request.session["paragraph"] = request.session["paragraph_matches"][request.session["sentence_pos"]]

                    CHOSEN_FILE = highlight_and_show(request.session["paragraph"], request.session['page_relation'])
                    SHOW_3 = True

                    if request.session["sentence_pos"] != 0:
                        SHOW_3_BACK = True


                if request.POST["button"] == 'answer_helpful':
                    question = QuestionLog(
                        query = request.session["query"],
                        answer = request.session["BERT_ANSWER"],
                        resource = Resource.objects.get(resource_name=request.POST['chosen_file']),
                        date = date.today()
                    )
                    question.save()
                    try:
                        os.remove('WebApp/temp_files/' + request.session["username"] + '_temp.pdf')
                    except:
                        pass
                    BERT_ANSWER = request.session['BERT_ANSWER']
                    SHOW_ANSWER = True


                if request.POST["button"] == 'answer_not_helpful':
                    paragraph = request.session["paragraph"]
                    CHOSEN_FILE = highlight_and_show(paragraph, request.session['page_relation'])
                    if request.session["bert_answer_pos"] != 4:
                        SHOW_ANSWER = True
                        request.session["bert_answer_pos"] += 1
                        request.session["BERT_ANSWER"] = request.session["all_bert_answers"][request.session["bert_answer_pos"]]["text"]
                        BERT_ANSWER = request.session["BERT_ANSWER"]
                        SHOW_4 = True
                    else:
                        SHOW_ERROR = True


        try:
            if request.session["question_variables_stored_in_session"]:
                try:
                    BERT_ANSWER = request.session["BERT_ANSWER"]
                except:
                    pass
                try:
                    SHOW_1 = request.session["SHOW_1"]
                except:
                    pass
                try:
                    SHOW_2 = request.session["SHOW_2"]
                except:
                    pass
                try:
                    SHOW_2_BACK = request.session["SHOW_2_BACK"]
                except:
                    pass
                try:
                    SHOW_3 = request.session["SHOW_3"]
                except:
                    pass
                try:
                    SHOW_3_BACK = request.session["SHOW_3_BACK"]
                except:
                    pass
                try:
                    SHOW_4 = request.session["SHOW_4"]
                except:
                    pass
                try:
                    SHOW_ANSWER = request.session["SHOW_ANSWER"]
                except:
                    pass
                try:
                    SHOW_ERROR = request.session["SHOW_ERROR"]
                except:
                    pass
                try:
                    CHOSEN_FILE = request.session["CHOSEN_FILE"]
                except:
                    pass
                if request.session["session_variable_limit"] == 0:
                    request.session["question_variables_stored_in_session"] = False
                else:
                    request.session["session_variable_limit"] -= 1
        except:
            pass
        print(CHOSEN_FILE)
        return render(request, "WebApp/askquestion.html", {
            'bert_answer': BERT_ANSWER,
            'show1': SHOW_1,
            'show2': SHOW_2,
            'show2_back': SHOW_2_BACK,
            'show3': SHOW_3,
            'show3_back': SHOW_3_BACK,
            'show_answer': SHOW_ANSWER,
            'show4': SHOW_4,
            'show_error': SHOW_ERROR,
            'chosen_file': CHOSEN_FILE,
            'name': request.session["name"],
            'loged_in': request.session['loged_in']})
    else:
        return redirect(choosefile)

@csrf_exempt
def get_text(request):
    extract_text_returned = WebApp.extract_text.get_page_text(request.session["chosen_file"])
    text = extract_text_returned[0]
    request.session["page_relation"] = extract_text_returned[1]

    data = {
        'text': text
    }
    return JsonResponse(data)

@csrf_exempt
def get_page_info(request):
    data = {
        'page': request.session['matches'][request.session['match_pos']].replace('.', '.\n\n'),
        'query': request.session['query']
    }
    return JsonResponse(data)

@csrf_exempt
def get_paragraph_info(request):
    data = {
        'paragraph': request.session["paragraph"],
        'query': request.session['query']
    }
    return JsonResponse(data)