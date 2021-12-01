import unittest
from unittest.mock import AsyncMock, patch

from sporepedia import api
from sporepedia.api import APIClient
from sporepedia.enums import SearchFilter


class APITest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._client = APIClient()

    @patch.object(APIClient, "_request")
    async def test_search(self, mock_request: AsyncMock):  # TODO
        mock_request.return_value.text.return_value = """throw 'allowScriptTagRemoting is false.';
//#DWR-INSERT
//#DWR-REPLY
var s1=[];var s0={};var s3={};var s4={};var s5=[];var s6={};var s7={};var s2={};var s8=[];s1[0]=s0;
s0.adventureStat=s3;s0.assetFunction='ADV_PUZZLE';s0.assetId=500377997389;s0.auditTrail=null;\
s0.author=s4;s0.created=new Date(1246035348779);s0.description="A psychic entity has you at\
 its disposal. What will it have you do? Now actually working!\
 Thanks for making this a rising star guys.EDIT: I haven\'t checked out this in a while!\
 Thanks for making this on the TOP PAGE! ";s0.featured=new Date(1247011200000);\
s0.id=500377997389;s0.imageCount=2;s0.localeString="en_US";s0.name="The Psychic Planet";\
s0.originalId=500377997764;s0.parentId=500377997764;s0.quality=true;s0.rating=14.376374;\
s0.requiredProducts=s5;s0.sourceIp="98.203.139.225";s0.status=s6;\
s0.tags="cool,fun,lava,psychic,puzzle,test";s0.thumbnailSize=41862;s0.type='ADVENTURE';\
s0.updated=new Date(1461858314548);
s3.adventureId=500377997389;s3.adventureLeaderboardId=500377997389;s3.difficulty=5;\
s3.lockedCaptainAssetId=null;s3.losses=104177;s3.pointValue=51;s3.totalPlays=157748;\
s3.updated=new Date(1371579201795);s3.wins=53571;
s4.assetCount=128;s4.avatarImage="thumb\\/500\\/335\\/938\\/500335938963.png";\
s4.avatarImageCustom=false;s4.dateCreated=new Date(1213754220000);s4['default']=true;\
s4.id=2262951433;s4.lastLogin=new Date(1337907125837);s4.name="Doomwaffle";\
s4.newestAssetCreated=new Date(1332451380361);s4.nucleusUserId=2262951433;s4.personaId=173842184;\
s4.screenName="Doomwaffle";s4.subscriptionCount=359;s4.tagline="Galactic Adventurer";\
s4.updated=new Date(1245989976725);s4.userId=2262951433;
s5[0]='EXPANSION_PACK1';s5[1]='INSECT_LIMBS';s5[2]='SPORE_CORE';
s6.declaringClass=s7;s6.name="CLASSIFIED";s6.nameKey="asset.status.classified";
s7.name="com.ea.sp.pollinator.db.Asset$Status";
s2['class com.ea.sp.pollinator.db.Asset']=s8;
s8[0]=s0;
dwr.engine._remoteHandleCallback('4','0',{resultSize:1,results:s1,resultsPerType:s2});
"""
        async with self._client as client:
            await client.search(
                text="test",
                lenght=20,
                params=api.SearchParams(
                    fields=api.FieldsSearchParam(
                        is_name=True,
                        is_author=True,
                        is_tag=True,
                    ),
                    functions=api.FunctionsSearchParam(
                        is_tribe_creature=True,
                        is_adventure_creature=True,
                        is_industry=True,
                        is_adv_collect=True,
                        is_adv_puzzle=True,
                        is_adv_template=True
                    ),
                    purposes=api.PurposesSearchParam(
                        is_military=True,
                        is_cultural=True,
                    ),
                ),
                filter=SearchFilter.featured,
                batch_id=4,
                adv=2
            )
