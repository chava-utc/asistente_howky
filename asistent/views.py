from django.shortcuts import render

def home(request):
    return render(request, 'index.html')


error_messages = {
    400: 'Hubo un problema con la solicitud que realizaste. Asegúrate de que la información enviada sea correcta y vuelve a intentarlo.',
    401: 'No tienes autorización para acceder a este recurso. Por favor, inicia sesión y asegúrate de tener los permisos adecuados.',
    403: 'No tienes permiso para acceder a esta página. Si crees que esto es un error, contacta con el administrador.',
    404: 'Lo sentimos, no pudimos encontrar la página que estás buscando. Verifica la URL o vuelve a la página de inicio.',
    405: 'El método de la solicitud no está permitido para este recurso. Verifica la forma en que intentas acceder y prueba de nuevo.',
    408: 'La solicitud tardó demasiado tiempo en completarse. Verifica tu conexión a internet e inténtalo nuevamente.',
    429: 'Has realizado demasiadas solicitudes en poco tiempo. Por favor, espera un momento antes de volver a intentarlo.',
    500: 'Ocurrió un problema en el servidor. Estamos trabajando para solucionarlo. Intenta nuevamente más tarde.',
    502: 'El servidor recibió una respuesta inválida al intentar procesar tu solicitud. Intenta de nuevo más tarde.',
    503: 'El servicio no está disponible en este momento debido a tareas de mantenimiento o sobrecarga. Por favor, vuelve a intentarlo más tarde.',
    504: 'El servidor no pudo obtener una respuesta a tiempo. Revisa tu conexión e intenta nuevamente más tarde.'
}

#Paginas de error -----------------------------------------------
def error_code_info(setCode):    
    codeList = {}
    error_code = 'error_code'
    
    codeList[error_code] = setCode
    
    if setCode in error_messages:
        codeList['error_info'] = error_messages[setCode]
    else:
        codeList['error_info'] = 'Error desconocido.'
    
    return codeList

def error_400(request, exception):
    setErrorCode = error_code_info(400)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=400)

def error_401(request):
    setErrorCode = error_code_info(401)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=401)

def error_403(request, exception):
    setErrorCode = error_code_info(403)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=403)

def error_404(request, exception):
    setErrorCode = error_code_info(404)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=404)

def error_405(request):
    setErrorCode = error_code_info(405)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=405)

def error_408(request):
    setErrorCode = error_code_info(408)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=408)

def error_429(request):
    setErrorCode = error_code_info(429)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=429)

def error_500(request):
    setErrorCode = error_code_info(500)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=500)

def error_502(request):
    setErrorCode = error_code_info(502)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=502)

def error_503(request):
    setErrorCode = error_code_info(503)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=503)

def error_504(request):
    setErrorCode = error_code_info(504)
    contexto = {**setErrorCode}
    return render(request, 'base/error_page.html', contexto, status=504)
