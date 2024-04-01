from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from src.models.student import StudentCollection, StudentModel, UpdateStudentModel
from src.database.database import student_collection
from bson import ObjectId


student_router = APIRouter(prefix='/student')

@student_router.get(
    "/all/",
    response_description="List all students",
    response_model=StudentCollection,
    response_model_by_alias=False,
)
def list_students():
    """
    List all of the student data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return StudentCollection(students= list(student_collection.find()))


@student_router.get(
    "/student/{id}",
    response_description="Get a single student",
    response_model=StudentModel,
    response_model_by_alias=False,
)
def show_student(id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    if (
        student :=  student_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@student_router.post(
    "/create/",
    response_description="Add new student",
    response_model=StudentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
def create_student(student: StudentModel = Body(...)):
    """
    Insert a new student record.

    A unique `id` will be created and provided in the response.
    """
    new_student = student_collection.insert_one(
        student.model_dump(by_alias=True, exclude=["id"])
    )
    created_student = student_collection.find_one(
        {"_id": new_student.inserted_id}
    )
    return created_student


@student_router.put(
    "/update/{id}",
    response_description="Update a student",
    response_model=StudentModel,
    response_model_by_alias=False,
)
def update_student(id: str, student: UpdateStudentModel = Body(...)):
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    student = {
        k: v for k, v in student.model_dump(by_alias=True).items() if v is not None
    }

    if len(student) >= 1:
        update_result = student_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": student},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_student := student_collection.find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@student_router.delete("/delete/{id}", response_description="Delete a student")
def delete_student(id: str):
    """
    Remove a single student record from the database.
    """
    delete_result = student_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")
