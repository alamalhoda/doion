from django.dispatch import Signal

verification_submitted = Signal()
verification_approved = Signal()
verification_rejected = Signal()
