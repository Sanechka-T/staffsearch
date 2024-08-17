from django import forms

from .models import Resume, WorkExperience, Education, About, ProfessionalSkills, Portfolio


class ResumeForm(forms.ModelForm):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))

    date_birth = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'class': 'form-control col-md-4',
                                                                                      'type': 'date'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Ваш номер телефона',
                                                                           'id': 'phone'}))
    city = forms.CharField(label='Город', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    post = forms.CharField(label='Должность', widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary = forms.DecimalField(label='Зарплата', widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                max_digits=10,
                                decimal_places=2)
    employment = forms.ChoiceField(label='Тип занятости', choices=Resume.EMPLOYMENT_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    removal = forms.BooleanField(label='Готовность к переезду', required=False,
                                 widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    remote_work = forms.BooleanField(label='Удалённая работа', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    resume_file = forms.FileField(label='Есть резюме на hh.ru? Просто перенесите его сюда!', required=False,
                                  widget=forms.FileInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Фотография', required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Resume
        fields = (
            'name', 'lastname', 'date_birth', 'phone', 'city', 'email', 'post', 'salary', 'employment', 'removal',
            'remote_work', 'resume_file', 'photo')


class WorkExperienceForm(forms.ModelForm):
    position = forms.CharField(label='Должность',required=False, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder':
                                                                                    'Например: Менеджер отдела'}))
    company_name = forms.CharField(label='Название компании',required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(label='Дата начала работы',required=False,
                                 widget=forms.DateInput(attrs={'class': 'form-control col-md-4',
                                                               'type': 'date'}))
    end_date = forms.DateField(label='Дата окончания работы', required=False,
                               widget=forms.DateInput(attrs={'class': 'form-control col-md-4',
                                                             'type': 'date',
                                                             'id': 'end_date'}))
    right_now = forms.BooleanField(label='По настоящее время', required=False,
                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                     'id': 'now'}))
    experience = forms.ChoiceField(label='Стаж', choices=WorkExperience.EXPERIENCE_CHOICES, required=False,
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    description = forms.CharField(label='Обязанности', required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                               'placeholder':
                                                                   'Опишите ваши обязанности на предыдущем месте работы...'}))
    achievements = forms.CharField(label='Достижения', required=False,
                                   widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                                'placeholder': 'Укажите ваши достижения и успехи...'}))

    class Meta:
        model = WorkExperience
        fields = (
            'position', 'company_name', 'start_date', 'end_date', 'right_now', 'experience',
            'description', 'achievements')


class EducationForm(forms.ModelForm):
    degree = forms.ChoiceField(label='Уровень образования', choices=Education.DEGREE_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-select'}))
    form_of_education = forms.ChoiceField(label='Форма обучения', choices=Education.EDUCATION_CHOICES,
                                          widget=forms.Select(attrs={'class': 'form-select'}))
    year_of_graduation = forms.CharField(label='Год окончания',
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    educational_institution = forms.CharField(label='Название учебного заведения',
                                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    faculty = forms.CharField(label='Факультет', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.CharField(label='Специальность', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Education
        fields = (
            'degree', 'form_of_education', 'year_of_graduation', 'educational_institution', 'faculty', 'specialty')


class AboutForm(forms.ModelForm):
    biography = forms.CharField(label='Дополнительные сведения', required=False,
                                widget=forms.Textarea(attrs={'class': 'form-control',
                                                             'placeholder':
                                                                 'Указывайте только те ваши личные качества,'
                                                                 'которые напрямую имеют отношение к вашей '
                                                                 'профессиональной деятельности. '
                                                                 'Например, менеджеру по работе с клиентами '
                                                                 'можно написать о коммуникабельности '
                                                                 'и умении находить общий язык '
                                                                 'с любым собеседником.'}))

    class Meta:
        model = About
        fields = ('biography',)


class ProfessionalSkillsForm(forms.ModelForm):
    skills = forms.CharField(label='Навыки',required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                                          'placeholder':
                                                                              'Перечислите ваши навыки через запятую...'}))

    class Meta:
        model = ProfessionalSkills
        fields = ('skills',)


class PortfolioForm(forms.ModelForm):
    description = forms.CharField(label='Описание работ', required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                               'placeholder':
                                                                   'Опишите все преимущества ваших работ...'}))

    class Meta:
        model = Portfolio
        fields = ('description',)
