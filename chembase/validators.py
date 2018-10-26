from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class CustomValidator(object):
    def __init__(self,forbidden_list):
        self.black_list=forbidden_list

    def validate(self, password, user=None):
        for item in self.black_list:
            if item.lower() in password.lower():
                raise ValidationError(
                    _("This password contains not allowed keyword: %(word)s"),
                    code='word_not_allowed',
                    params={'word': item},
                )

    def get_help_text(self):
        return _(
            "Your password cannot be the same as the default password."
        ) 
