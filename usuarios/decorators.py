from django.shortcuts import redirect

def perfil_requerido(perfil):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            try:

                if request.user.perfilusuario.perfil == perfil:

                    return view_func(
                        request,
                        *args,
                        **kwargs
                    )

            except:
                pass

            return redirect('/login/')

        return wrapper

    return decorator