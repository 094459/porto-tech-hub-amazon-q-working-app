from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import Survey, SurveyOption, SurveyResponse
from forms import CreateSurveyForm, SurveyResponseForm
from models.database import db
from models.survey import Survey
from . import survey_bp

@survey_bp.route('/surveys')
@login_required
def list():
    surveys = Survey.query.filter_by(user_id=current_user.user_id).all()
    return render_template('survey/list.html', surveys=surveys)

@survey_bp.route('/surveys/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateSurveyForm()
    if form.validate_on_submit():
        survey = Survey(
            user_id=current_user.user_id,
            title=form.title.data,
            description=form.description.data
        )
        db.session.add(survey)
        db.session.commit()

        for i, option in enumerate(form.options.data, start=1):
            survey_option = SurveyOption(
                survey_id=survey.survey_id,
                option_text=option,
                option_order=i
            )
            db.session.add(survey_option)
        db.session.commit()

        flash('Survey created successfully!', 'success')
        return redirect(url_for('survey.list'))
    return render_template('survey/create.html', form=form)

@survey_bp.route('/surveys/<int:survey_id>')
@login_required
def view(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if survey.user_id != current_user.user_id:
        abort(403)
    return render_template('survey/view.html', survey=survey)

@survey_bp.route('/feedback/<int:survey_id>', methods=['GET', 'POST'])
def feedback(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if not survey.is_active:
        flash('This survey is no longer active.', 'error')
        return redirect(url_for('main.index'))

    form = SurveyResponseForm()
    form.option.choices = [(str(o.option_id), o.option_text) for o in survey.options]

    if form.validate_on_submit():
        response = SurveyResponse(
            survey_id=survey_id,
            option_id=int(form.option.data),
            respondent_email=form.email.data
        )
        db.session.add(response)
        db.session.commit()

        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('main.index'))

    return render_template('survey/feedback.html', survey=survey, form=form)