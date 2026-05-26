from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid



# ╔══════════════════════════════════════════════════════════════════════╗
# ║                          USUARIOS                                    ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ══════════════════════════════════════════════════════
# ROL
# Diagrama: PK id_roles, nombre_roles
# ══════════════════════════════════════════════════════
class Rol(models.Model):

    nombre_rol = models.CharField(
        max_length=150,
        unique=True
    )

    permisos = models.ManyToManyField(
        'Permiso',
        through='RolPermiso',
        related_name='roles'
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    actualizado_en = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = 'roles'

        verbose_name = 'Rol'

        verbose_name_plural = 'Roles'

        ordering = ['nombre_rol']

    def __str__(self):

        return self.nombre_rol


# ══════════════════════════════════════════════════════
# PERMISO
# Diagrama: PK id_permiso, descripcion, slug (UNIQUE)
# ══════════════════════════════════════════════════════
class Permiso(models.Model):
    descripcion = models.CharField(max_length=150)
    slug        = models.SlugField(max_length=150, unique=True)

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'permisos'
        verbose_name        = 'Permiso'
        verbose_name_plural = 'Permisos'
        ordering            = ['slug']

    def __str__(self):
        return f"{self.slug} — {self.descripcion}"


# ══════════════════════════════════════════════════════
# ROL PERMISO  (tabla pivote Rol ↔ Permiso  N:M)
# Diagrama: PK id_rolpermisos, FK id_permisos, FK id_roles
# ══════════════════════════════════════════════════════
class RolPermiso(models.Model):
    rol     = models.ForeignKey(Rol,     on_delete=models.CASCADE, related_name='rol_permisos')
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE, related_name='rol_permisos')

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'rol_permisos'
        verbose_name        = 'Rol-Permiso'
        verbose_name_plural = 'Roles-Permisos'
        unique_together     = [('rol', 'permiso')]

    def __str__(self):
        return f"{self.rol.nombre_rol} → {self.permiso.slug}"


# ══════════════════════════════════════════════════════
# USUARIO
# Diagrama: PK id_usuario, FK id_roles, nombres_usuario,
#           apellidos_usuario, correo_usuario,
#           numero_documento, contrasena,
#           tipo_documento, estado_usuario
# ══════════════════════════════════════════════════════
class Usuario(models.Model):

    ESTADO_CHOICES = [
        ('ACTIVO',   'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    TIPO_DOCUMENTO_CHOICES = [
        ('CC',  'Cédula de Ciudadanía'),
        ('CE',  'Cédula de Extranjería'),
        ('TI',  'Tarjeta de Identidad'),
        ('PA',  'Pasaporte'),
        ('NIT', 'NIT'),
    ]

    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='usuarios'
    )

    nombres_usuario   = models.CharField(max_length=150)
    apellidos_usuario = models.CharField(max_length=150, blank=True, null=True)
    correo_usuario    = models.EmailField(max_length=150, unique=True)
    numero_documento  = models.CharField(max_length=150, blank=True, null=True)
    tipo_documento    = models.CharField(max_length=150, choices=TIPO_DOCUMENTO_CHOICES, blank=True, null=True)
    contrasena        = models.CharField(max_length=150)

    estado_usuario = models.CharField(max_length=150, choices=ESTADO_CHOICES, default='ACTIVO')

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'usuarios'
        verbose_name        = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering            = ['-creado_en']

    def __str__(self):
        return f"{self.get_full_name()} ({self.correo_usuario})"

    def set_password(self, raw_password: str) -> None:
        self.contrasena = make_password(raw_password)

    def get_full_name(self) -> str:
        return f"{self.nombres_usuario} {self.apellidos_usuario or ''}".strip()

    @property
    def is_admin(self) -> bool:
        return bool(self.rol and self.rol.nombre_rol.upper() == 'ADMINISTRADOR')

    @property
    def is_cliente(self) -> bool:
        return bool(self.rol and self.rol.nombre_rol.upper() == 'CLIENTE')

    @property
    def activo(self) -> bool:
        return self.estado_usuario == 'ACTIVO'

    def tiene_permiso(self, slug: str) -> bool:
        """Verifica si el rol del usuario tiene un permiso específico por slug."""
        if not self.rol:
            return False
        return RolPermiso.objects.filter(rol=self.rol, permiso__slug=slug).exists()


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                          CATÁLOGO                                    ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ══════════════════════════════════════════════════════
# PROVEEDOR
# Diagrama: PK id_proovedor, nit_proovedor (UNIQUE),
#           nombre_proovedor, telefono_proovedor, 
#           correo_proovedor
# ══════════════════════════════════════════════════════
class Proveedor(models.Model):
    nit_proveedor      = models.BigIntegerField(unique=True)
    nombre_proveedor   = models.CharField(max_length=150)
    telefono_proveedor = models.BigIntegerField()
    correo_proveedor   = models.EmailField(max_length=150)

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'proveedores'
        verbose_name        = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering            = ['nombre_proveedor']

    def __str__(self):
        return f"{self.nombre_proveedor} (NIT: {self.nit_proveedor})"


# ══════════════════════════════════════════════════════
# CATÁLOGO
# Diagrama: PK id_catalogo, nombre_catalogo
# Relación: Catalogo 1:N Producto
# ══════════════════════════════════════════════════════
class Catalogo(models.Model):
    nombre_catalogo      = models.CharField(max_length=150)
    descripcion_catalogo = models.TextField(blank=True, null=True)
    creado_en            = models.DateTimeField(auto_now_add=True)
    actualizado_en       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'catalogos'
        verbose_name        = 'Catálogo'
        verbose_name_plural = 'Catálogos'
        ordering            = ['nombre_catalogo']

    def __str__(self):
        return self.nombre_catalogo


# ══════════════════════════════════════════════════════
# CATEGORÍA
# Diagrama: FK en Producto → id_categoria
# Mejora: + estado + descripcion + auditoría (del proyecto viejo)
# ══════════════════════════════════════════════════════
class Categoria(models.Model):

    ESTADO_CHOICES = [
        ('ACTIVO',   'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    nombre      = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    estado      = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'categorias'
        verbose_name        = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering            = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def activo(self) -> bool:
        return self.estado == 'ACTIVO'


# ══════════════════════════════════════════════════════
# PRODUCTO
# Diagrama: PK id_producto, FK id_proovedor,
#           FK id_categoria, nombre_producto,
#           descripcion_producto
# IMPORTANTE: El stock y precio viven en VariacionProducto.
# Mejora: + FK catalogo, + estado, + foto, + auditoría
# ══════════════════════════════════════════════════════
class Producto(models.Model):

    ESTADO_CHOICES = [
        ('DISPONIBLE',    'Disponible'),
        ('NO_DISPONIBLE', 'No Disponible'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.RESTRICT,   related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,    related_name='productos')
    catalogo  = models.ForeignKey(Catalogo,  on_delete=models.SET_NULL,   related_name='productos', null=True, blank=True)

    nombre_producto      = models.CharField(max_length=150)
    descripcion_producto = models.TextField(blank=True, null=True)

    foto   = models.CharField(max_length=500, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'productos'
        verbose_name        = 'Producto'
        verbose_name_plural = 'Productos'
        ordering            = ['-creado_en']

    def __str__(self):
        return self.nombre_producto

    @property
    def foto_url(self) -> str | None:
        return f"/imagenes/{self.foto}" if self.foto else None

    @property
    def disponible(self) -> bool:
        return self.estado == 'DISPONIBLE'

    @property
    def stock_total(self) -> int:
        """Stock total sumado de todas las variaciones."""
        from django.db.models import Sum
        resultado = self.variaciones.aggregate(total=Sum('stock_actual'))
        return resultado['total'] or 0

    
    def actualizar_estado(self):

        variaciones = self.variaciones.all()

        disponible = variaciones.filter(
            stock_actual__gte=models.F('stock_minimo')
        ).exists()

        if disponible:
            self.estado = 'DISPONIBLE'
        else:
            self.estado = 'NO_DISPONIBLE'


# ══════════════════════════════════════════════════════
# VARIACIÓN DE PRODUCTO
# Diagrama: PK id_variaciones, FK id_producto,
#           talla, color, sku_unico (UNIQUE),
#           precio_compra, precio_base, iva_porcentaje,
#           stock_actual, stock_minimo
# CLAVE: aquí viven el stock y los precios reales.
# ══════════════════════════════════════════════════════
class VariacionProducto(models.Model):

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variaciones')

    talla     = models.CharField(max_length=5)
    color     = models.CharField(max_length=150)
    sku_unico = models.CharField(max_length=150, unique=True)

    precio_compra  = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    precio_base    = models.FloatField(validators=[MinValueValidator(0.01)])
    iva_porcentaje = models.FloatField(default=19.0, validators=[MinValueValidator(0.0)])

    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        producto = self.producto

        producto.actualizar_estado()

        producto.save(update_fields=['estado', 'actualizado_en'])
            
    


    class Meta:
        db_table            = 'variacion_producto'
        verbose_name        = 'Variación de Producto'
        verbose_name_plural = 'Variaciones de Producto'
        ordering            = ['producto', 'talla', 'color']

    def __str__(self):
        return f"{self.producto.nombre_producto} | {self.talla} - {self.color} (SKU: {self.sku_unico})"

    @property
    def precio_con_iva(self) -> int:
        return int(self.precio_base * (1 + self.iva_porcentaje / 100))
    
    
    @property
    def bajo_stock(self) -> bool:
        return self.stock_actual <= self.stock_minimo

    @property
    def sin_stock(self) -> bool:
        return self.stock_actual <= 0


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                         INVENTARIO                                   ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ══════════════════════════════════════════════════════
# ENTRADA  (compra de mercancía a proveedor)
# Diagrama: PK id_entrada, FK id_proovedor,
#           fecha_entrada, total_entrada
# Relación: Proveedor 1:N Entrada
# ══════════════════════════════════════════════════════
class Entrada(models.Model):

    proveedor     = models.ForeignKey(Proveedor, on_delete=models.RESTRICT, related_name='entradas')
    fecha_entrada = models.DateTimeField()
    total_entrada = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'entradas'
        verbose_name        = 'Entrada de Inventario'
        verbose_name_plural = 'Entradas de Inventario'
        ordering            = ['-fecha_entrada']

    def __str__(self):
        return f"Entrada #{self.id} — {self.proveedor.nombre_proveedor} ({self.fecha_entrada.strftime('%d/%m/%Y')})"

    @property
    def total_calculado(self) -> int:
        from django.db.models import Sum
        resultado = self.detalles.aggregate(total=Sum('cantidades'))
        return resultado['total'] or 0

    def recalcular_total(self) -> None:
        self.total_entrada = self.total_calculado
        self.save(update_fields=['total_entrada'])


# ══════════════════════════════════════════════════════
# DETALLE ENTRADA
# Diagrama: PK id_detalle, FK id_entrada,
#           FK id_variaciones, cantidades,
#           precio_comprado
# Relación: Entrada 1:N DetalleEntrada
#           VariacionProducto 1:N DetalleEntrada
# ══════════════════════════════════════════════════════
class DetalleEntrada(models.Model):

    entrada   = models.ForeignKey(Entrada,           on_delete=models.CASCADE,  related_name='detalles')
    variacion = models.ForeignKey(VariacionProducto, on_delete=models.RESTRICT, related_name='detalles_entrada')

    cantidades      = models.IntegerField(validators=[MinValueValidator(1)])
    precio_comprado = models.IntegerField(validators=[MinValueValidator(0)])

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'detalle_entrada'
        verbose_name        = 'Detalle de Entrada'
        verbose_name_plural = 'Detalles de Entrada'

    def __str__(self):
        return f"Entrada #{self.entrada.id} | {self.variacion.sku_unico} × {self.cantidades}"

    def aplicar_stock(self) -> None:

        self.variacion.stock_actual += self.cantidades
        self.variacion.save(update_fields=['stock_actual', 'actualizado_en'])

        producto = self.variacion.producto
        if producto.estado == 'NO_DISPONIBLE' and self.variacion.stock_actual >= self.variacion.stock_minimo:
            producto.estado = 'DISPONIBLE'
            producto.save(update_fields=['estado', 'actualizado_en'])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                           VENTAS                                     ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ══════════════════════════════════════════════════════
# VENTA
# Diagrama: PK id_venta, FK id_usuario, fecha,
#           subtotal, descuento_fidelidad,
#           monto_iva, monto_final
# ══════════════════════════════════════════════════════
class Venta(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='ventas')

    fecha               = models.DateTimeField(auto_now_add=True)
    subtotal            = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    descuento_fidelidad = models.FloatField(default=0.0, validators=[MinValueValidator(0)], blank=True, null=True)
    monto_iva           = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    monto_final         = models.FloatField(default=0.0, validators=[MinValueValidator(0)])

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'ventas'
        verbose_name        = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering            = ['-fecha']

    def __str__(self):
        return f"Venta #{self.id} — {self.usuario.get_full_name()} ({self.fecha.strftime('%d/%m/%Y')})"

    @property
    def total_venta(self) -> float:
        return self.monto_final

    @property
    def cantidad_productos(self) -> int:
        from django.db.models import Sum
        resultado = self.detalles.aggregate(cant=Sum('cantidad'))
        return resultado['cant'] or 0

    def recalcular_totales(self) -> None:
        """
        Recalcula subtotal, monto_iva y monto_final
        desde los detalles. Llamar tras guardar todos los DetalleVenta.
        """
        subtotal = sum(d.subtotal for d in self.detalles.all())
        self.subtotal    = subtotal
        self.monto_iva   = round(subtotal * 0.19, 2)
        descuento        = self.descuento_fidelidad or 0
        self.monto_final = round(subtotal + self.monto_iva - descuento, 2)
        self.save(update_fields=['subtotal', 'monto_iva', 'monto_final', 'actualizado_en'])


# ══════════════════════════════════════════════════════
# DETALLE VENTA
# Diagrama: PK id_detalle, FK id_variaciones,
#           FK id_ventas, cantidad, precio_unitario
# CAMBIO CLAVE: FK → VariacionProducto (no Producto directo)
# ══════════════════════════════════════════════════════
class DetalleVenta(models.Model):

    venta     = models.ForeignKey(Venta,             on_delete=models.CASCADE,  related_name='detalles')
    variacion = models.ForeignKey(VariacionProducto, on_delete=models.RESTRICT, related_name='detalles_venta')

    cantidad        = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.FloatField(validators=[MinValueValidator(0)])

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'detalle_venta'
        verbose_name        = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    def __str__(self):
        return f"{self.cantidad}× {self.variacion.sku_unico} — ${self.precio_unitario:,.0f}"

    @property
    def subtotal(self) -> float:
        return self.cantidad * self.precio_unitario

    def descontar_stock(self) -> None:
        """
        Descuenta el stock de la variación al confirmar la venta.
        Llamar dentro de transaction.atomic().
        """
        if self.variacion.stock_actual < self.cantidad:
            raise ValueError(
                f"Stock insuficiente para '{self.variacion}'. "
                f"Disponible: {self.variacion.stock_actual}, solicitado: {self.cantidad}."
            )
        self.variacion.stock_actual -= self.cantidad
        self.variacion.save(update_fields=['stock_actual', 'actualizado_en'])

        producto = self.variacion.producto
        producto.actualizar_estado()
        producto.save(update_fields=['estado', 'actualizado_en'])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                           ENVÍOS                                     ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ══════════════════════════════════════════════════════
# ENVÍO
# Diagrama: PK id_envio, FK id_usuario, FK id_venta,
#           departamento_envio, ciudad_envio,
#           barrio_envio, direccion_envio,
#           tipo_vivienda, especificaciones_llegada,
#           telefono_llegada, empresa_transportadora,
#           numero_guia, estado_envio,
#           fecha_envio, fecha_estipulada_llegada
# Relación: Venta 1:1 Envio  /  Usuario 1:N Envio
# ══════════════════════════════════════════════════════
class Envio(models.Model):

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_CAMINO', 'En Camino'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
        ('DEVUELTO',  'Devuelto'),
    ]

    TIPO_VIVIENDA_CHOICES = [
        ('CASA',        'Casa'),
        ('APARTAMENTO', 'Apartamento'),
        ('OFICINA',     'Oficina'),
        ('LOCAL',       'Local Comercial'),
        ('OTRO',        'Otro'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT,  related_name='envios')
    venta   = models.OneToOneField(Venta, on_delete=models.CASCADE,  related_name='envio')

    departamento_envio = models.CharField(max_length=150)
    ciudad_envio       = models.CharField(max_length=150)
    barrio_envio       = models.CharField(max_length=150, blank=True, null=True)
    direccion_envio    = models.CharField(max_length=150)
    tipo_vivienda      = models.CharField(max_length=150, choices=TIPO_VIVIENDA_CHOICES, default='CASA')

    especificaciones_llegada = models.TextField(max_length=200, blank=True, null=True)
    telefono_llegada         = models.CharField(max_length=200)

    empresa_transportadora = models.CharField(max_length=150, blank=True, null=True)
    numero_guia            = models.CharField(max_length=150, blank=True, null=True, unique=True)

    estado_envio             = models.CharField(max_length=150, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_envio              = models.DateTimeField()
    fecha_estipulada_llegada = models.DateField()

    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    creado_en      = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'envios'
        verbose_name        = 'Envío'
        verbose_name_plural = 'Envíos'
        ordering            = ['-fecha_envio']

    def __str__(self):
        return (
            f"Envío #{self.id} — Venta #{self.venta.id} | "
            f"{self.ciudad_envio}, {self.departamento_envio} "
            f"[{self.get_estado_envio_display()}]"
        )

    @property
    def entregado(self) -> bool:
        return self.estado_envio == 'ENTREGADO'

    @property
    def en_transito(self) -> bool:
        return self.estado_envio == 'EN_CAMINO'

    @property
    def direccion_completa(self) -> str:
        partes = [self.direccion_envio]
        if self.barrio_envio:
            partes.append(f"Barrio {self.barrio_envio}")
        partes += [self.ciudad_envio, self.departamento_envio]
        return ', '.join(partes)




# ══════════════════════════════════════════════════════
# TOKEN RESET — Restablecimiento de contraseña
# ══════════════════════════════════════════════════════
class TokenReset(models.Model):
    usuario   = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tokens_reset')
    token     = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    usado     = models.BooleanField(default=False)

    class Meta:
        db_table = 'tokens_reset'

    def esta_vigente(self):
        from datetime import timedelta
        import datetime
        ahora = datetime.datetime.now()
        return not self.usado and ahora < self.creado_en + timedelta(hours=24)

    def __str__(self):
        return f"Token de {self.usuario.correo_usuario}"