from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import role_required
from consultas.models import Consulta, SignosVitales
from .models import HistorialMedico, Usuario, Area
from django.db.models import Count
from .forms import HistorialMedicoForm
import plotly.express as px
import plotly.graph_objects as go
import re

def login_view(request):
    token = {
        "correo": r'^((ib|im|ii|ie|isc|lg|am)[0-9]{6}@itsatlixco\.edu\.mx)|(^admin[0-9]@admin\.com)|^([0-9]{6}@itsatlixco\.edu\.mx)$',
        "password": r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&ñ_])[A-Za-z\d@$!%*#?&ñ_]{8,15}$'
    }
    # Si ya hay una sesión iniciada, redirigir al dashboard del rol correspondiente
    if request.user.is_authenticated:
        if request.user.role.nombre_rol == "medico":
            return redirect("medico_dashboard")  # Nombre de la vista para médicos
        elif request.user.role.nombre_rol == "paciente":
            return redirect("paciente_dashboard")  # Nombre de la vista para pacientes

    if request.method == "POST":
        ''' Si el formulario es enviado se autentica el usuario '''
        email = request.POST.get("email")
        password = request.POST.get("password")
        token_email_valido = re.match(token["correo"], email)
        token_password_valido = re.match(token["password"], password)

        if not token_email_valido:
            messages.error(request, "Correo no válido.")
            return redirect("login")
        if not token_password_valido:
            messages.error(request, "Contraseña no válida.")
            return redirect("login")

        if token_email_valido and token_password_valido:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                # Redirigir según el rol del usuario
                if user.role.nombre_rol == "medico":
                    return redirect("medico_dashboard")  # Nombre de la vista para médicos
                elif user.role.nombre_rol == "paciente":
                    return redirect("paciente_dashboard")  # Nombre de la vista para pacientes
                elif user.role.nombre_rol == "admin":
                    return redirect("/admin/")
                else:
                    messages.error(request, "Rol no reconocido.")
                    return redirect("login")
            else:
                messages.error(request, "Credenciales inválidas.")
    return render(request, "login.html")


def logout_view(request):
    # if request.user.is_authenticated:
    logout(request)
    return redirect("login")


@login_required
@role_required(["medico"])
def medico_dashboard(request):
    usuarios = Usuario.objects.filter(role__nombre_rol='paciente')  # Filtrar solo pacientes
    cantidad_usuarios = usuarios.count()
    cant_hombres = usuarios.filter(sexo='M').count()  # Cantidad de hombres
    cant_mujeres = usuarios.filter(sexo='F').count()  # Cantidad de mujeres
    genero_data = usuarios.values('sexo').annotate(total=Count('sexo'))  # Cantidad de usuarios por género
    genero_fig = px.pie(  # Gráfica de pastel
        values=[g['total'] for g in genero_data],  # Cantidad de usuarios por género
        names=['Masculino' if g['sexo'] == 'M' else 'Femenino' for g in genero_data],  # Nombres de género
        title="Distribución de Género"
    )

    # Pacientes con hábitos
    historiales = HistorialMedico.objects.all()  # Todos los historiales médicos
    habitos = {  # Filtro de los hábitos de los pacientes
        'Fuman': historiales.filter(usa_cigarro=True).count(),  # Cantidad de pacientes que fuman
        'Ingiere Alcohol': historiales.filter(ingiere_alcohol=True).count(),  # Cantidad de pacientes que ingieren alcohol
        'Usa Drogas': historiales.filter(usa_drogas=True).count(),  # Cantidad de pacientes que usan drogas
        'Embarazadas': historiales.filter(es_embarazada=True).count(),  # Cantidad de pacientes embarazadas
    }
    # Gráfica de barras
    habitos_fig = go.Figure([go.Bar(x=list(habitos.keys()), y=list(habitos.values()), marker_color='indianred')])
    # Personalización de gráfica
    habitos_fig.update_layout(title_text="Pacientes con Hábitos", xaxis_title="Hábito", yaxis_title="Cantidad")

    # Tipos de consultas
    # Cantidad de pacientes por tipo de consulta
    consultas = Consulta.objects.values('tipo_de_consulta').annotate(total=Count('tipo_de_consulta'))
    consultas_fig = px.pie(  # Gráfica de pastel
        values=[c['total'] for c in consultas],  # Cantidad de pacientes por tipo de consulta
        names=['Médica' if c['tipo_de_consulta'] == 'M' else 'Asesoría' for c in consultas],  # Nombres de tipos de consulta
        title="Distribución de Tipos de Consultas"
    )

    # Gráfica de barras de cantidad de pacientes por area
    carrera_o_puesto = Usuario.objects.values('carrera_o_puesto_id').annotate(total=Count('carrera_o_puesto_id'))
    areas_fig = go.Figure([go.Bar(x=[c['carrera_o_puesto_id'] for c in carrera_o_puesto], y=[c['total'] for c in carrera_o_puesto], marker_color='indianred')])
    areas_fig.update_layout(title_text="Distribución de Areas", xaxis_title="Area", yaxis_title="Cantidad")

    # Pasar gráficas como HTML al template
    return render(request, 'medico_dashboard.html', {
        'genero_graph': genero_fig.to_html(full_html=False),  # Gráfica de pastel
        'cantidad_usuarios': cantidad_usuarios,
        'cant_hombres': cant_hombres,
        'cant_mujeres': cant_mujeres,
        'habitos_graph': habitos_fig.to_html(full_html=False),  # Gráfica de barras
        'consultas_graph': consultas_fig.to_html(full_html=False),  # Gráfica de pastel
        'areas_graph': areas_fig.to_html(full_html=False),
        'pacientes_areas': areas_fig.to_html(full_html=False),
    })

@login_required
@role_required(["paciente"])
def paciente_dashboard(request):
    return render(request, "paciente_dashboard.html")


@login_required
@role_required(["paciente"])
def historial_view(request):
    # obtener el historial médico del paciente
    historial = request.user.historial
    return render(request, "historial_medico.html", {"historial": historial})


@login_required
@role_required(["paciente"])
def paciente_consultas(request):
    consultas = Consulta.objects.filter(clave_paciente=request.user)
    signos = SignosVitales.objects.filter(consulta__clave_paciente=request.user)
    return render(request, "paciente_consultas.html", {"consultas": consultas, "signos": signos})


@login_required
@role_required(["paciente", "medico"])
def usuario_informacion(request):
    informacion = request.user
    return render(request, "informacion.html", {"informacion": informacion})


@login_required
@role_required(["paciente", "medico"])
def cambiar_contrasena(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$', new_password):
            messages.error(request, "La contraseña debe tener al entre 8 y 15 caracteres, incluir una letra mayúscula, un número y un caracter especial.")
            return redirect("informacion")
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$', confirm_password):
            messages.error(request, "La contraseña debe tener al entre 8 y 15 caracteres, incluir una letra mayúscula, un número y un caracter especial.")
            return redirect("informacion")

        if not request.user.check_password(current_password):
            error_message = 'La contraseña actual es incorrecta.'
            return render(request, "informacion.html", {
                'informacion': request.user,
                'error': error_message
            })

        if new_password != confirm_password:
            error_message = 'Las contraseñas no coinciden.'
            return render(request, "informacion.html", {
                'informacion': request.user,
                'error': error_message
            })

        request.user.set_password(new_password)
        request.user.save()
        # Mantener la sesión activa después del cambio de contraseña
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
        return redirect("informacion")

    return redirect("informacion")


@login_required
@role_required(["medico"])
def medico_consultas(request):
    mostrar_todas = request.GET.get('todas', '0') == '1'  # Leer parámetro 'todas'
    if mostrar_todas:
        consultas = Consulta.objects.select_related('clave_medico', 'clave_paciente', 'signos_vitales').all()
    else:
        consultas = Consulta.objects.select_related('clave_medico', 'clave_paciente', 'signos_vitales').filter(clave_medico=request.user)

    return render(request, "medico_consultas.html", {
        "consultas": consultas,
        "mostrar_todas": mostrar_todas
    })


@login_required
@role_required(["medico"])
def medico_historiales(request):
    query = request.GET.get('search', '')
    # Si hay una consulta, filtrar los historiales de acuerdo a la consulta
    if query:
        historiales = HistorialMedico.objects.filter(id_historial__icontains=query)
    else:
        historiales = HistorialMedico.objects.all()
    return render(request, "medico_historiales.html", {"historiales": historiales, "query": query})


@login_required
@role_required(["medico"])
def editar_historial(request, pk):
    historial = get_object_or_404(HistorialMedico, id_historial=pk)
    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            return redirect('medico_historiales')  # Cambia a la URL de tu vista principal
    else:
        form = HistorialMedicoForm(instance=historial)
    return render(request, 'editar_historial.html', {'form': form, 'historial': historial})