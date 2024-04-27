from django.contrib import admin

from .models import Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, Track

# Register your models here
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Genre)
admin.site.register(Invoice)
admin.site.register(InvoiceLine)
admin.site.register(MediaType)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(Track)

# Register your models here.
