from django.contrib import admin
from django.utils.html import format_html
from .models import Book, BorrowInfo, Comment

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("BookID", "BookName", "category", "Publisher", "ReleaseDate", "Status", "cover_preview") 
    list_filter = ("Status", "category", "Publisher") 
    search_fields = ("BookName", "Publisher")

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="100" style="border-radius: 5px;" />', obj.cover_image.url)
        return "No Cover"
    cover_preview.short_description = "Cover Preview"

    fieldsets = (
        (None, {
            'fields': ("BookName", "Publisher", "category", "ReleaseDate", "Amount", "InStock", "Status", "cover_image", "description") 
        }),
    )

@admin.register(BorrowInfo)
class BorrowInfoAdmin(admin.ModelAdmin):
    list_display = ("Number", "BookID", "get_user_id", "BorrowTime", "ReturnTime", "ActualReturnTime", "Status")
    search_fields = ("BookID__BookName", "BorrowUserID__user_id")
    list_filter = ("Status",)

    def get_user_id(self, obj):
        return obj.BorrowUserID.user_id
    get_user_id.short_description = "BorrowUserID"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("BookID", "BorrowUserID", "Comment", "CommentTime")
    search_fields = ("BookID__BookName", "BorrowUserID__username")
    list_filter = ("BookID", "BorrowUserID")
