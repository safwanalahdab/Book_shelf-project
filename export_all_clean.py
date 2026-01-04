import json
from pathlib import Path
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookshelf.settings")
django.setup()

from django.contrib.auth.models import User
from books.models import Author, Category, Book, BorrowedBook, Favorite_Book


def to_fixture(model_label: str, pk: int, fields: dict) -> dict:
    return {"model": model_label, "pk": pk, "fields": fields}


out = []

# 1) Author
for a in Author.objects.all().order_by("id"):
    out.append(to_fixture("books.author", a.pk, {"name": a.name}))

# 2) Category
for c in Category.objects.all().order_by("id"):
    out.append(to_fixture("books.category", c.pk, {"name": c.name}))

# 3) Book (ننقل مسار الصورة كنص فقط)
for b in Book.objects.all().order_by("id"):
    out.append(
        to_fixture(
            "books.book",
            b.pk,
            {
                "title": b.title,
                "description": b.description,
                "image": str(b.image) if b.image else "",
                "author": b.author_id,
                "category": b.category_id,
                "total_copies": b.total_copies,
                "available_copies": b.available_copies,
                "count_borrowed": b.count_borrowed,
                "created_at": b.created_at.isoformat() if b.created_at else None,
                "is_avaiable": b.is_avaiable,
                "possition": b.possition,
                "is_archived": b.is_archived,
                "pages": b.pages,
                "publication_year": b.publication_year,
                "isbn": b.isbn,
            },
        )
    )

# 4) User (اختياري بس أنا بنقله لأن Borrowed/Favorite بيعتمد عليه)
# ننقل أهم الحقول + password hash (بيخلي تسجيل الدخول يشتغل بنفس كلمة السر)
for u in User.objects.all().order_by("id"):
    out.append(
        to_fixture(
            "auth.user",
            u.pk,
            {
                "password": u.password,
                "last_login": u.last_login.isoformat() if u.last_login else None,
                "is_superuser": u.is_superuser,
                "username": u.username,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
                "is_staff": u.is_staff,
                "is_active": u.is_active,
                "date_joined": u.date_joined.isoformat() if u.date_joined else None,
                "groups": [g.pk for g in u.groups.all()],
                "user_permissions": [p.pk for p in u.user_permissions.all()],
            },
        )
    )

# 5) BorrowedBook
for bb in BorrowedBook.objects.all().order_by("id"):
    out.append(
        to_fixture(
            "books.borrowedbook",
            bb.pk,
            {
                "book": bb.book_id,
                "borrower": bb.borrower_id,
                "borrow_date": bb.borrow_date.isoformat() if bb.borrow_date else None,
                "return_date": bb.return_date.isoformat() if bb.return_date else None,
                "is_returned": bb.is_returned,
                "notes": bb.notes or "",
                "return_request": bb.return_request,
                "return_request_date": bb.return_request_date.isoformat() if bb.return_request_date else None,
                "due_date": bb.due_date.isoformat() if bb.due_date else None,
            },
        )
    )

# 6) Favorite_Book
for f in Favorite_Book.objects.all().order_by("id"):
    out.append(
        to_fixture(
            "books.favorite_book",  # انتبه: Django بيحوّل Favorite_Book -> favorite_book
            f.pk,
            {
                "user": f.user_id,
                "book": f.book_id,
                "created_at": f.created_at.isoformat() if f.created_at else None,
            },
        )
    )

Path("all_clean_fixture.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(f"Exported {len(out)} objects to all_clean_fixture.json")
