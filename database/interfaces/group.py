from . import Interface
from MADI.models import Group
from database.schemas import group, schedule


class GroupsDB(Interface):
    
    async def get_schedule_data(self, id:int):
        query = schedule.select()
        print('asdawd')
        return await self.db.fetch_all(query=query)

DBGroups = GroupsDB(
    model=Group,
    schema=group
    )


