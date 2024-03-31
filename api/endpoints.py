from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from io import StringIO
import logging
import json

from models.db_models import Route
from db import new_route, get_db, get_route_by_id
from utils import simulated_annealing

# logging
logger = logging.getLogger(__name__)

# routers
router = APIRouter()


@router.post("/routes")
async def create_route(file: UploadFile = File(None), data: str = Form(None), format: str = None, db: AsyncSession = Depends(get_db)):

    # check if file or data is provided
    if format and format == "csv":
        if file is None:
            raise HTTPException(status_code=400, detail="CSV file is required")
        else:
            try:
                # prepare data
                file_data = [x.split(",") for x in StringIO(str(file.file.read(), 'utf-8')).readlines()]
                header = file_data[0]
                data = file_data[1:]
                data_dicts = [{k:(float(v) if k in ["lat", "lng"] else v) for k, v in zip(header, row)} for row in data]

                # check if data is valid
                if len(data_dicts) < 3:
                    raise HTTPException(status_code=400, detail="At least three points are required")
                
                # calculate route
                simulate = simulated_annealing(data_dicts)

                # save route and return
                result = [data_dicts[i] for i in simulate[0]]
                row = await new_route(Route(points=result), db=db)
                return row
        
            except Exception as e:
                logger.exception(str(e))
                raise HTTPException(status_code=400, detail=str(e))
            
    
    elif data:
        try:
            # prepare data
            points_dict = json.loads(data)

            # check if data is valid
            if len(points_dict['points']) < 3:
                raise HTTPException(status_code=400, detail="At least three points are required")
            
            # calculate route
            simulate = simulated_annealing(points_dict['points'])

            # save route and return
            result = [points_dict['points'][i] for i in simulate[0]]
            row = await new_route(Route(points=result), db=db)
            return row

        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Payload must be a valid JSON string")
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
                logger.exception(str(e))
                raise HTTPException(status_code=400, detail=str(e))
    else: 
        raise HTTPException(status_code=400, detail="Either file or data must be provided")
    

@router.get("/routes/{id}")
async def get_routes_by_id(id: int = None, db: AsyncSession = Depends(get_db)):
    if id:
        route = await get_route_by_id(id, db)
        if route:
            return route
        raise HTTPException(status_code=404, detail="Route not found")
    else:
        raise HTTPException(status_code=400, detail="id must be provided")
        