import pytest
from app import db
from app.modules.notepad import models, repositories

REPO = repositories.NotepadRepository()

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        db.session.query(models.Notepad).delete()
        db.session.add(models.Notepad(title="Notepad 1", body="Cuerpo 1", user_id=1))
        db.session.add(models.Notepad(title="Notepad 2", body="Cuerpo 2", user_id=1))
        db.session.commit()

    yield test_client


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"

def test_get_all_notepads():
    notepads = REPO.get_all_by_user(1)
    assert len(notepads) == 2
    assert notepads[0].title == "Notepad 1"
    
def test_create_notepad():
    cantidadInicial = len(REPO.get_all_by_user(1))
    nuevoNotepad = REPO.create(title="Nuevo notepad", body="Nuevo cuerpo", user_id=1)
    
    assert len(REPO.get_all_by_user(1)) == cantidadInicial + 1
    assert nuevoNotepad in REPO.get_all_by_user(1)
    assert nuevoNotepad.title == "Nuevo notepad"
        
def test_create_uses_sequential_ids():
    ultimaId = REPO.get_all_by_user(1)[-1].id
    nuevoNotepad = REPO.create(title="Nuevo notepad", body="Nuevo notepad", user_id=1)
    
    assert ultimaId + 1 == nuevoNotepad.id

def test_update_notepad():
    
    notepad = REPO.get_by_id(1)
    updatedNotepad = REPO.update(1, title="Titulo actualizado")
    
    assert updatedNotepad.title == "Titulo actualizado"
    assert notepad.body == updatedNotepad.body
    
def test_delete_notepad():
    
    cantidadInicial = len(REPO.get_all_by_user(1))
    borrado = REPO.delete(1)
    
    assert len(REPO.get_all_by_user(1)) == cantidadInicial - 1
    assert borrado is True
