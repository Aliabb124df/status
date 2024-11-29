from django.urls import path
from .views import family_register,send_email_view,dead_register,marriage_register,birth_register,show_marriage_register,divorce_register,choose_document,get_document,show_documents,review_task,send_notes,done_task,insert_document,insert_task,refuse_with_note,dead_register_show,show_new_documents,delete_document

urlpatterns = [
   
    path('family_register',family_register ,name='family_register'),
    path('send_email_view',send_email_view ,name='send_email_view'),
    path('dead_register',dead_register ,name='dead_register'),
    path('marriage_register',marriage_register ,name='marriage_register'),
    path('birth_register',birth_register ,name='birth_register'),
    path('show_marriage_register',show_marriage_register ,name='show_marriage_register'),
    path('divorce_register', divorce_register,name='divorce_register'),
    path('choose_document', choose_document,name='choose_document'),
    path('get_document', get_document,name='get_document'),
    path('show_documents', show_documents,name='show_documents'),
    path('review_task',review_task,name='review_task'),
    path('send_notes', send_notes,name='send_notes'),
    path('done_task', done_task,name='done_task'),
    path('insert_document',insert_document ,name='insert_document'),
    path('insert_task', insert_task,name='insert_task'),
    path('refuse_with_note',refuse_with_note ,name='refuse_with_note'),
    path('dead_register_show', dead_register_show,name='dead_register_show'),
    path('show_new_documents', show_new_documents,name='show_new_documents'),
    path('delete_document', delete_document,name='delete_document'),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),

]