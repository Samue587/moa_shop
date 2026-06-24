from locust import HttpUser, task, between


class UsuarioMOA(HttpUser):
    wait_time = between(1, 3)

    host = "http://127.0.0.1:8000"

    # =========================
    # LOGIN (IMPORTANTE: primero)
    # =========================
    def on_start(self):
        self.login()

    def on_start(self):
        r = self.client.get("/login/")
        csrftoken = r.cookies["csrftoken"]

        self.client.post("/login/", {
            "correo_usuario": "samuel@test.com",
            "contrasena": "123Castillo*"
        }, headers={"X-CSRFToken": csrftoken})
    # =========================
    # TIENDA (NO /productos/)
    # =========================
    @task(3)
    def ver_tienda(self):
        self.client.get("/tienda/")

    @task(2)
    def ver_producto(self):
        # usa un endpoint real de tu proyecto
        self.client.get("/tienda/producto/2/")

    @task(2)
    def buscar_productos(self):
        # OJO: tu sistema no tiene /productos/
        self.client.get("/tienda/?search=camisa adidas 12")

    @task(2)
    def ver_carrito(self):
        self.client.get("/carrito/")

    @task(1)
    def checkout(self):
        self.client.get("/checkout/")