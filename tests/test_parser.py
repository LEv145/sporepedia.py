from typing import cast
import unittest

from js2py.base import JsObjectWrapper

from sporepedia.errors import DwrParserError
from sporepedia.parser import SporeDwrEngineParser


class TestSporeDwrEngineParsers(unittest.TestCase):

    def test_1(self):  # TODO: Name?
        parser = SporeDwrEngineParser()

        text = """throw 'allowScriptTagRemoting is false.';
//#DWR-REPLY
if (window.dwr) dwr.engine._remoteHandleBatchException({ \
name:'org.directwebremoting.extend.ServerException', \
message:'The specified call count is not a number' });
else if (window.parent.dwr) window.parent.dwr.engine._remoteHandleBatchException({ \
name:'org.directwebremoting.extend.ServerException', \
message:'The specified call count is not a number' });
"""

        try:
            parser.parse(text)
        except Exception as error:
            self.assertIsInstance(error, DwrParserError)
            self.assertEqual(cast(DwrParserError, error).message, "The specified call count is not a number")
            self.assertEqual(cast(DwrParserError, error).name, "org.directwebremoting.extend.ServerException")

    def test_2(self):
        parser = SporeDwrEngineParser()

        text = """throw 'allowScriptTagRemoting is false.';
//#DWR-INSERT
//#DWR-REPLY
var s3=[];var s1={};var s5={};var s6=[];var s0={};var s7={};\
var s2={};var s8={};var s9=[];var s4={};var s10=[];s3[0]=s1;s3[1]=s2;
s1.adventureStat=null;s1.assetFunction='CITY_HALL';s1.assetId=500586138735;\
s1.auditTrail=null;s1.author=s5;s1.created=new Date(1273147355612);\
s1.description="test, test, test. Kann mir mal einer sagen ob die Kreation online gestellt wurde?";\
s1.featured=null;s1.id=500586138735;s1.imageCount=1;s1.localeString="de_DE";s1.name="Test";\
s1.originalId=500586138735;s1.parentId=null;s1.quality=false;s1.rating=null;s1.requiredProducts=s6;\
s1.sourceIp=null;s1.status=s0;s1.tags="hungersnot, test";s1.thumbnailSize=23637;\
s1.type='BUILDING';s1.updated=new Date(1273147355597);
s5.assetCount=1768;s5.avatarImage="thumb\\/500\\/470\\/438\\/500470438972.png";\
s5.avatarImageCustom=false;s5.dateCreated=new Date(1214650140000);\
s5['default']=true;s5.id=2263769540;s5.lastLogin=new Date(1397251419188);s5.name="Hungersnot";\
s5.newestAssetCreated=new Date(1299428796992);s5.nucleusUserId=2263769540;s5.personaId=174473339;\
s5.screenName="Hungersnot";s5.subscriptionCount=161;\
s5.tagline="Einzugestehen dass man etwas nicht wei\u00DF ist Wissen";\
s5.updated=new Date(1278487634765);s5.userId=2263769540;
s6[0]='SPORE_CORE';
s0.declaringClass=s7;s0.name="CLASSIFIED";s0.nameKey="asset.status.classified";
s7.name="com.ea.sp.pollinator.db.Asset$Status";
s2.adventureStat=null;s2.assetFunction='CITY_HALL';s2.assetId=500198868984;s2.auditTrail=null;\
s2.author=s8;s2.created=new Date(1227979603997);s2.description="Color eye test, what is the answer?";\
s2.featured=null;s2.id=500198868984;s2.imageCount=1;s2.localeString=null;s2.name="Color eye test";\
s2.originalId=null;s2.parentId=500198771887;s2.quality=false;s2.rating=-1.0;s2.requiredProducts=s9;\
s2.sourceIp=null;s2.status=s0;s2.tags="eye test";s2.thumbnailSize=22217;s2.type='BUILDING';\
s2.updated=new Date(1227979603997);
s8.assetCount=768;s8.avatarImage="thumb\\/500\\/655\\/246\\/500655246178.png";s8.avatarImageCustom=false;\
s8.dateCreated=new Date(1213730460000);s8['default']=true;s8.id=2259901423;\
s8.lastLogin=new Date(1606135213248);s8.name="DeKDeS";s8.newestAssetCreated=new Date(1420413732605);\
s8.nucleusUserId=2259901423;s8.personaId=173794308;s8.screenName="DeKDeS";s8.subscriptionCount=246;\
s8.tagline="No longer active";s8.updated=new Date(1433801298020);s8.userId=2259901423;
s9[0]='SPORE_CORE';
s4['class com.ea.sp.pollinator.db.Asset']=s10;
s10[0]=s1;s10[1]=s2;
dwr.engine._remoteHandleCallback('8','0',{resultSize:2846,results:s3,resultsPerType:s4});"""

        outlog, errorlog = parser.parse(text)
        self.assertIsNone(errorlog)

        self.assertEqual(
            outlog,
            JsObjectWrapper({
                "resultSize": 2846,
                "results": [
                    {
                        "adventureStat": None,
                        "assetFunction": "CITY_HALL",
                        "assetId": 500586138735,
                        "auditTrail": None,
                        "author": {
                            "assetCount": 1768,
                            "avatarImage": "thumb/500/470/438/500470438972.png",
                            "avatarImageCustom": False,
                            "dateCreated": {},
                            "default": True,
                            "id": 2263769540,
                            "lastLogin": {},
                            "name": "Hungersnot",
                            "newestAssetCreated": {},
                            "nucleusUserId": 2263769540,
                            "personaId": 174473339,
                            "screenName": "Hungersnot",
                            "subscriptionCount": 161,
                            "tagline": "Einzugestehen dass man etwas nicht weiß ist Wissen",
                            "updated": {},
                            "userId": 2263769540,
                        },
                        "created": {},
                        "description": "test, test, test. Kann mir mal einer sagen ob die Kreation online gestellt wurde?",
                        "featured": None,
                        "id": 500586138735,
                        "imageCount": 1,
                        "localeString": "de_DE",
                        "name": "Test",
                        "originalId": 500586138735,
                        "parentId": None,
                        "quality": False,
                        "rating": None,
                        "requiredProducts": ["SPORE_CORE"],
                        "sourceIp": None,
                        "status": {
                            "declaringClass": {"name": "com.ea.sp.pollinator.db.Asset$Status"},
                            "name": "CLASSIFIED",
                            "nameKey": "asset.status.classified",
                        },
                        "tags": "hungersnot, test",
                        "thumbnailSize": 23637,
                        "type": "BUILDING",
                        "updated": {},
                    },
                    {
                        "adventureStat": None,
                        "assetFunction": "CITY_HALL",
                        "assetId": 500198868984,
                        "auditTrail": None,
                        "author": {
                            "assetCount": 768,
                            "avatarImage": "thutypemb/500/655/246/500655246178.png",
                            "avatarImageCustom": False,
                            "dateCreated": {},
                            "default": True,
                            "id": 2259901423,
                            "lastLogin": {},
                            "name": "DeKDeS",
                            "newestAssetCreated": {},
                            "nucleusUserId": 2259901423,
                            "personaId": 173794308,
                            "screenName": "DeKDeS",
                            "subscriptionCount": 246,
                            "tagline": "No longer active",
                            "updated": {},
                            "userId": 2259901423,
                        },
                        "created": {},
                        "description": "Color eye test, what is the answer?",
                        "featured": None,
                        "id": 500198868984,
                        "imageCount": 1,
                        "localeString": None,
                        "name": "Color eye test",
                        "originalId": None,
                        "parentId": 500198771887,
                        "quality": False,
                        "rating": -1,
                        "requiredProducts": ["SPORE_CORE"],
                        "sourceIp": None,
                        "status": {
                            "declaringClass": {"name": "com.ea.sp.pollinator.db.Asset$Status"},
                            "name": "CLASSIFIED",
                            "nameKey": "asset.status.classified",
                        },
                        "tags": "eye test",
                        "thumbnailSize": 22217,
                        "type": "BUILDING",
                        "updated": {},
                    },
                ],
                "resultsPerType": {
                    "class com.ea.sp.pollinator.db.Asset": [
                        {
                            "adventureStat": None,
                            "assetFunction": "CITY_HALL",
                            "assetId": 500586138735,
                            "auditTrail": None,
                            "author": {
                                "assetCount": 1768,
                                "avatarImage": "thumb/500/470/438/500470438972.png",
                                "avatarImageCustom": False,
                                "dateCreated": {},
                                "default": True,
                                "id": 2263769540,
                                "lastLogin": {},
                                "name": "Hungersnot",
                                "newestAssetCreated": {},
                                "nucleusUserId": 2263769540,
                                "personaId": 174473339,
                                "screenName": "Hungersnot",
                                "subscriptionCount": 161,
                                "tagline": "Einzugestehen dass man etwas nicht weiß ist Wissen",
                                "updated": {},
                                "userId": 2263769540,
                            },
                            "created": JsObjectWrapper({}),
                            "description": "test, test, test. Kann mir mal einer sagen ob die Kreation online gestellt wurde?",
                            "featured": None,
                            "id": 500586138735,
                            "imageCount": 1,
                            "localeString": "de_DE",
                            "name": "Test",
                            "originalId": 500586138735,
                            "parentId": None,
                            "quality": False,
                            "rating": None,
                            "requiredProducts": ["SPORE_CORE"],
                            "sourceIp": None,
                            "status": {
                                "declaringClass": {"name": "com.ea.sp.pollinator.db.Asset$Status"},
                                "name": "CLASSIFIED",
                                "nameKey": "asset.status.classified",
                            },
                            "tags": "hungersnot, test",
                            "thumbnailSize": 23637,
                            "type": "BUILDING",
                            "updated": JsObjectWrapper({}),
                        },
                        JsObjectWrapper({
                            "adventureStat": None,
                            "assetFunction": "CITY_HALL",
                            "assetId": 500198868984,
                            "auditTrail": None,
                            "author": JsObjectWrapper({
                                "assetCount": 768,
                                "avatarImage": "thumb/500/655/246/500655246178.png",
                                "avatarImageCustom": False,
                                "dateCreated": JsObjectWrapper({}),
                                "default": True,
                                "id": 2259901423,
                                "lastLogin": JsObjectWrapper({}),
                                "name": "DeKDeS",
                                "newestAssetCreated": JsObjectWrapper({}),
                                "nucleusUserId": 2259901423,
                                "personaId": 173794308,
                                "screenName": "DeKDeS",
                                "subscriptionCount": 246,
                                "tagline": "No longer active",
                                "updated": JsObjectWrapper({}),
                                "userId": 2259901423,
                            }),
                            "created": JsObjectWrapper({}),
                            "description": "Color eye test, what is the answer?",
                            "featured": None,
                            "id": 500198868984,
                            "imageCount": 1,
                            "localeString": None,
                            "name": "Color eye test",
                            "originalId": None,
                            "parentId": 500198771887,
                            "quality": False,
                            "rating": -1,
                            "requiredProducts": ["SPORE_CORE"],
                            "sourceIp": None,
                            "status": JsObjectWrapper({
                                "declaringClass": JsObjectWrapper(
                                    {"name": "com.ea.sp.pollinator.db.Asset$Status"}
                                ),
                                "name": "CLASSIFIED",
                                "nameKey": "asset.status.classified",
                            }),
                            "tags": "eye test",
                            "thumbnailSize": 22217,
                            "type": "BUILDING",
                            "updated": JsObjectWrapper({}),
                        }),
                    ]
                },
            })
        )
