from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing
from core.locust.common import fake, get_csrf_token
from bs4 import BeautifulSoup

class NotepadBehavior(TaskSet):
    def on_start(self):
        self.login()
        self.last_notepad_id = None

    def login(self):
        response = self.client.get("/login")
        if response.status_code != 200:
            print(f"Login page failed: {response.status_code}")
            return

        csrf_token = get_csrf_token(response)
        response = self.client.post(
            "/login",
            data={
                "email": "user1@example.com",
                "password": "1234",
                "csrf_token": csrf_token
            },
            allow_redirects=True
        )
        if response.status_code != 200:
            print(f"Login failed: {response.status_code}")

    @task(3)
    def list_notepads(self):
        response = self.client.get("/notepad")
        if response.status_code != 200:
            print(f"List notepads failed: {response.status_code}")

    @task(2)
    def create_notepad(self):
        response = self.client.get("/notepad/create")
        csrf_token = get_csrf_token(response)

        data = {
            "title": fake.sentence(nb_words=4),
            "body": fake.paragraph(nb_sentences=2),
            "csrf_token": csrf_token
        }
        response = self.client.post("/notepad/create", data=data, allow_redirects=True)
        if response.status_code != 200:
            print(f"Create notepad failed: {response.status_code}")
            return

        # Extraer el id del último notepad creado
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            edit_link = soup.find("a", string="Edit")
            if edit_link:
                href = edit_link.get("href")
                self.last_notepad_id = href.rstrip("/").split("/")[-1]
        except Exception:
            self.last_notepad_id = None

    @task(1)
    def edit_notepad(self):
        if not self.last_notepad_id:
            return

        response = self.client.get(f"/notepad/edit/{self.last_notepad_id}")
        csrf_token = get_csrf_token(response)

        data = {
            "title": fake.sentence(nb_words=5),
            "body": fake.paragraph(nb_sentences=3),
            "csrf_token": csrf_token
        }
        response = self.client.post(f"/notepad/edit/{self.last_notepad_id}", data=data, allow_redirects=True)
        if response.status_code != 200:
            print(f"Edit notepad failed: {response.status_code}")

    @task(1)
    def delete_notepad(self):
        if not self.last_notepad_id:
            return
        response = self.client.get(f"/notepad/edit/{self.last_notepad_id}")
        csrf_token = get_csrf_token(response)

        response = self.client.post(
            f"/notepad/delete/{self.last_notepad_id}",
            data={"csrf_token": csrf_token},
            allow_redirects=True
        )
        if response.status_code != 200:
            print(f"Delete notepad failed: {response.status_code}")
        else:
            self.last_notepad_id = None

class NotepadUser(HttpUser):
    tasks = [NotepadBehavior]
    wait_time = between(2, 5)
    host = get_host_for_locust_testing()
