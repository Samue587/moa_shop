from django.urls import path
from AppMoa import views

urlpatterns = [

    # ══════════════════════════════════════════════════════
    # AUTH
    # ══════════════════════════════════════════════════════
    path('',          views.home,          name='inicio'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('registro/', views.registro_view, name='registro'),

    # ══════════════════════════════════════════════════════
    # RESTABLECIMIENTO DE CONTRASEÑA
    # ══════════════════════════════════════════════════════
    path('password-reset/', views.solicitar_reset, name='password_reset'),
    path('password-reset/done/', views.reset_enviado, name='reset_enviado'),
    path('reset-password/<uuid:token>/', views.confirmar_reset, name='confirmar_reset'),
    path('reset-password/complete/', views.reset_completo, name='reset_completo'),

    # ══════════════════════════════════════════════════════
    # TIENDA PÚBLICA
    # ══════════════════════════════════════════════════════
    path('tienda/',                           views.tienda,           name='tienda'),
    path('tienda/producto/<int:id>/',         views.detalle_producto, name='detalle_producto'),

    # ══════════════════════════════════════════════════════
    # PERFIL DE USUARIO
    # ══════════════════════════════════════════════════════
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # ══════════════════════════════════════════════════════
    # CARRITO
    # ══════════════════════════════════════════════════════
    path('carrito/',                                   views.carrito_ver,        name='carrito_ver'),
    path('carrito/agregar/',                           views.carrito_agregar,    name='carrito_agregar'),
    path('carrito/actualizar/<int:variacion_id>/',     views.carrito_actualizar, name='carrito_actualizar'),
    path('carrito/remover/<int:variacion_id>/',        views.carrito_remover,    name='carrito_remover'),
    path('carrito/limpiar/',                           views.carrito_limpiar,    name='carrito_limpiar'),

    # ══════════════════════════════════════════════════════
    # CHECKOUT
    # ══════════════════════════════════════════════════════
    path('checkout/',                            views.checkout_procesar,    name='checkout_formulario'),
    path('checkout/procesar/',                   views.checkout_procesar,    name='checkout_procesar'),
    path('checkout/comprobante/<int:venta_id>/', views.checkout_comprobante, name='checkout_comprobante'),

    # ══════════════════════════════════════════════════════
    # PANEL ADMIN — DASHBOARD
    # ══════════════════════════════════════════════════════
    path('admin/dashboard/',       views.panel_admin,     name='admin_dashboard'),
    path('admin/dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),

    # ══════════════════════════════════════════════════════
    # ADMIN — ROLES
    # ══════════════════════════════════════════════════════
    path('admin/roles/',                   views.listar_roles,  name='admin_roles'),
    path('admin/roles/crear/',             views.crear_rol,     name='crear_rol'),
    path('admin/roles/editar/<int:id>/',   views.editar_rol,    name='editar_rol'),
    path('admin/roles/eliminar/<int:id>/', views.eliminar_rol,  name='eliminar_rol'),

    # ══════════════════════════════════════════════════════
    # ADMIN — PERMISOS
    # ══════════════════════════════════════════════════════
    path('admin/permisos/',                   views.listar_permisos,  name='admin_permisos'),
    path('admin/permisos/crear/',             views.crear_permiso,    name='crear_permiso'),
    path('admin/permisos/editar/<int:id>/',   views.editar_permiso,   name='editar_permiso'),
    path('admin/permisos/eliminar/<int:id>/', views.eliminar_permiso, name='eliminar_permiso'),

    # ══════════════════════════════════════════════════════
    # ADMIN — USUARIOS
    # ══════════════════════════════════════════════════════
    path('admin/usuarios/',                   views.listar_usuarios,  name='admin_usuarios'),
    path('admin/usuarios/crear/',             views.crear_usuario,    name='crear_usuario'),
    path('admin/usuarios/editar/<int:id>/',   views.editar_usuario,   name='editar_usuario'),
    path('admin/usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # ══════════════════════════════════════════════════════
    # ADMIN — PROVEEDORES
    # ══════════════════════════════════════════════════════
    path('admin/proveedores/',                   views.listar_proveedores,  name='admin_proveedores'),
    path('admin/proveedores/crear/',             views.crear_proveedor,     name='crear_proveedor'),
    path('admin/proveedores/editar/<int:id>/',   views.editar_proveedor,    name='editar_proveedor'),
    path('admin/proveedores/eliminar/<int:id>/', views.eliminar_proveedor,  name='eliminar_proveedor'),

    # ══════════════════════════════════════════════════════
    # ADMIN — CATÁLOGOS
    # ══════════════════════════════════════════════════════
    path('admin/catalogos/',                   views.listar_catalogos,  name='admin_catalogos'),
    path('admin/catalogos/crear/',             views.crear_catalogo,    name='crear_catalogo'),
    path('admin/catalogos/editar/<int:id>/',   views.editar_catalogo,   name='editar_catalogo'),
    path('admin/catalogos/eliminar/<int:id>/', views.eliminar_catalogo, name='eliminar_catalogo'),

    # ══════════════════════════════════════════════════════
    # ADMIN — CATEGORÍAS
    # ══════════════════════════════════════════════════════
    path('admin/categorias/',                   views.listar_categorias,  name='admin_categorias'),
    path('admin/categorias/crear/',             views.crear_categoria,    name='crear_categoria'),
    path('admin/categorias/editar/<int:id>/',   views.editar_categoria,   name='editar_categoria'),
    path('admin/categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # ══════════════════════════════════════════════════════
    # ADMIN — PRODUCTOS
    # ══════════════════════════════════════════════════════
    path('admin/productos/',                   views.listar_productos,  name='admin_productos'),
    path('admin/productos/crear/',             views.crear_producto,    name='crear_producto'),
    path('admin/productos/editar/<int:id>/',   views.editar_producto,   name='editar_producto'),
    path('admin/productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # ══════════════════════════════════════════════════════
    # ADMIN — VARIACIONES DE PRODUCTO
    # ══════════════════════════════════════════════════════
    path('admin/productos/<int:producto_id>/variaciones/',                   views.listar_variaciones,  name='admin_variaciones'),
    path('admin/productos/<int:producto_id>/variaciones/crear/',             views.crear_variacion,     name='crear_variacion'),
    path('admin/productos/<int:producto_id>/variaciones/editar/<int:id>/',   views.editar_variacion,    name='editar_variacion'),
    path('admin/productos/<int:producto_id>/variaciones/eliminar/<int:id>/', views.eliminar_variacion,  name='eliminar_variacion'),

    # ══════════════════════════════════════════════════════
    # ADMIN — INVENTARIO (entradas de mercancía)
    # ══════════════════════════════════════════════════════
    path('admin/inventario/',                   views.listar_entradas,  name='admin_inventario'),
    path('admin/inventario/crear/',             views.crear_entrada,    name='crear_entrada'),
    path('admin/inventario/detalle/<int:id>/',  views.detalle_entrada,  name='detalle_entrada'),
    path('admin/inventario/eliminar/<int:id>/', views.eliminar_entrada, name='eliminar_entrada'),

    # ══════════════════════════════════════════════════════
    # ADMIN — VENTAS
    # ══════════════════════════════════════════════════════
    path('admin/ventas/',                    views.listar_ventas,         name='admin_ventas'),
    path('admin/ventas/detalle/<int:id>/',   views.detalle_venta,         name='detalle_venta'),
    path('admin/ventas/exportar/excel/',     views.exportar_ventas_excel, name='exportar_ventas_excel'),
    path('admin/ventas/exportar/pdf/',       views.exportar_ventas_pdf,   name='exportar_ventas_pdf'),

    # ══════════════════════════════════════════════════════
    # ADMIN — ENVÍOS
    # ══════════════════════════════════════════════════════
    path('admin/envios/',                    views.listar_envios,        name='admin_envios'),
    path('admin/envios/detalle/<int:id>/',   views.detalle_envio,        name='detalle_envio'),
    path('admin/envios/editar/<int:id>/',    views.editar_envio,         name='editar_envio'),
    path('admin/envios/eliminar/<int:id>/',  views.eliminar_envio,       name='eliminar_envio'),
    path('admin/envios/estado/<int:id>/',    views.envio_cambiar_estado, name='envio_cambiar_estado'),

    # ══════════════════════════════════════════════════════
    # ADMIN — REPORTES
    # ══════════════════════════════════════════════════════
    path('admin/reportes/inventario/', views.reporte_inventario, name='reporte_inventario'),
    path('admin/reportes/ventas/',     views.reporte_ventas,     name='reporte_ventas'),
    path('admin/reportes/categorias/', views.reporte_categorias, name='reporte_categorias'),
    path('admin/reportes/envios/',     views.reporte_envios,     name='reporte_envios'),
    path('admin/reportes/clientes/',   views.reporte_clientes,   name='reporte_clientes'),
    path('admin/reportes/',            views.reportes_hub,       name='reportes_hub'),
]