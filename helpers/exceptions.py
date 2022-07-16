from fastapi import HTTPException


def raise_not_found(get_entity):
    def inner(*args, **kwargs):
        db_data = get_entity(*args, **kwargs)
        if db_data == None:
            raise HTTPException(status_code=404, detail={
                                "message": "Not Found"})
        return db_data
    return inner
