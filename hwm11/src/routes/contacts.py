import asyncio

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import Contact, Roles
from src.schemas import ContactModel, ResponseContact, ContactDb, UpdateContactRoleModel
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.services.roles import RolesChecker

router = APIRouter(prefix="/contacts", tags=["contacts"])

allowed_get_contacts = RolesChecker([Roles.admin, Roles.moderator, Roles.user])
allowed_create_contact = RolesChecker([Roles.admin, Roles.moderator, Roles.user])
allowed_get_contact_by_id = RolesChecker([Roles.admin, Roles.moderator, Roles.user])
allowed_update_contact = RolesChecker([Roles.admin, Roles.moderator])
allowed_change_contact_role = RolesChecker([Roles.admin, Roles.moderator])
allowed_delete_contact = RolesChecker([Roles.admin])


@router.post(
    "/create",
    response_model=ResponseContact,
    name="Create contact",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allowed_create_contact)],
)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    check_mail = repository_contacts.check_exist_mail(body, db)
    if check_mail:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Such mail already registered",
        )
    contact = await repository_contacts.create_contact(body, db)
    return {"contact": contact, "detail": "Contact was created"}


@router.get(
    "/",
    response_model=List[ContactDb],
    name="All contacts",
    dependencies=[Depends(allowed_get_contacts)],
)
async def get_contacts(
    db: Session = Depends(get_db),
    current_contact: Contact = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactDb,
    name="Get contact",
    dependencies=[Depends(allowed_get_contact_by_id)],
)
async def get_contact_by_id(
    contact_id: int = Path(1, ge=1),
    db: Session = Depends(get_db),
    current_contact: Contact = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return contact


@router.put(
    "/update/{contact_id}",
    response_model=ContactDb,
    name="Change contact",
    dependencies=[Depends(allowed_update_contact)],
)
async def update_contact(
    body: ContactModel,
    contact_id: int = Path(1, ge=1),
    db: Session = Depends(get_db),
    current_contact: Contact = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch(
    "/change_role/{contact_id}",
    response_model=ContactDb,
    name="Change role",
    dependencies=[Depends(allowed_change_contact_role)],
)
async def change_contact_role(
    body: UpdateContactRoleModel,
    contact_id: int = Path(1, ge=1),
    db: Session = Depends(get_db),
    current_contact: Contact = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.change_contact_role(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete(
    "/delete/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete contact",
    dependencies=[Depends(allowed_delete_contact)],
)
async def delete_contact(
    contact_id: int = Path(1, ge=1),
    db: Session = Depends(get_db),
    current_contact: Contact = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get(
    "/search_first_name/{inquiry}",
    response_model=List[ContactDb],
    name="Search by first name",
)
async def search_first_name(
    inquiry: str = Path(min_length=1),
    db: Session = Depends(get_db),
    current_contact: Contact = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.search_first_name(inquiry, db)
    if bool(contacts) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get(
    "/search_last_name/{inquiry}",
    response_model=List[ContactDb],
    name="Search by last name",
)
async def search_last_name(
    inquiry: str = Path(min_length=1),
    db: Session = Depends(get_db),
    current_contact: Contact = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.search_last_name(inquiry, db)
    if bool(contacts) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get(
    "/search_mail/{inquiry}",
    response_model=ContactDb,
    name="Search by email",
)
async def search_email(
    inquiry: str = Path(min_length=1),
    db: Session = Depends(get_db),
    current_contact: Contact = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.search_by_mail(inquiry, db)
    if bool(contacts) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts
