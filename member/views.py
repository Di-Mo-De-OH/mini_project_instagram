from django.contrib.auth import get_user_model
from django.core import signing
from django.core.signing import SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView
from utils.email import send_email

from member.forms import SignUpForm

User = get_user_model()


# Create your views here.
class SignUpView(FormView):
    template_name = "auth/signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        # 이메일 발송이 되어야함
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}'
        subject = "[Pystagram] 이메일 인증을 완료해주세요"
        message = f"다음 링크를 클릭해주세요.<br><a href='{url}'>url</a>"

        send_email(subject,message,user.email)

        return render(
            self.request,
            template_name="auth/signup_done.html",
        )

    def verify_email(request):
        code = request.GET.get("code", "")
        # 원래는 None 값이 들어와야함
        signer = TimestampSigner()
        try:
            decoded_user_email = signing.loads(code)
            email = signer.unsign(decoded_user_email, max_age=60 * 30)
        except (TypeError, SignatureExpired):
            return render(request, "auth/not_verified.html")
        user = get_object_or_404(User, email=email, is_active=False)
        user.is_active = True
        user.save()
        #TODO: 나중에 REdirect 시키기 로그인으로
        return render(request, "auth/email_verified_done.html", {"user": user})
