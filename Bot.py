import asyncio
import websockets
import json
import Twitch

IP_ADDR = "0.0.0.0"
IP_PORT = "8421"

global state
global Test_group
global sunshine_group
global streamer

state = False#<------------------------------------this need to be set correctly when you start your server
Test_group = xxxxxxxxxx
sunshine_group = xxxxxxxxxxx
streamer = 'sunshinebread'#your streamer name here

def Set_Level():
    global sunshine_group
    global Test_group
    print("choose the mode to start with[DEBUG/NORMAL]")
    while(True):
        level = input()
        if level == "DEBUG":
            sunshine_group = Test_group
            print("DEBUG mode starts!")
            return
        if level == "NORMAL":
            print("NORMAL mode starts!")
            return
        else:
            print("don't know what are u talking about")

async def send_group_at_all_msg(websocket,group_id,content):
    global streamer
    data = {
        "action":"send_group_msg",
        "params":
        {
            "group_id":group_id,
            "message":
            [
            {"type": "at","data": {"qq":"all"}},
            {"type": "text","data": {"text": f"{content}"}}
            ]
        }
    }
    print(f'\nsending group msg\n')
    state = True
    await websocket.send(json.dumps(data))

async def send_group_to_msg(websocket,group_id,content):
    global streamer
    data = {
        "action":"send_group_msg",
        "params":
            {
                "group_id":group_id,
                "message":{"type": "text","data": {"text": f"{content}"}}
            }
        }
    print(f'\ntriggered by private message\n')
    await websocket.send(json.dumps(data))

async def mainfunc(websocket):
    # main_function
    global sunshine_group
    global Test_group
    global state
    global streamer
    while True:
        recv_text = await websocket.recv()
        recv_text = json.loads(recv_text)
        # recv_text = json.dumps(recv_text,indent = 2)
        print(recv_text)

        if (recv_text.get("sub_type") == "friend"):
            await send_group_to_msg(websocket,Test_group,"i am still alive!")
            return
            #only to check the Bot live condition with my phone
            #this msg will be send to my test group in any condition

        game,title = Twitch.check_online(f'{streamer}')
        print(f'game: {game}\ntitle:{title}')

        if game:#this means streamer is alive
            if state == False:#this means havn't sent it
                await send_group_at_all_msg(websocket,sunshine_group,f"{streamer} went alive,{game},{title}")
                state = True#so send it and also change the state

        else:#this means streamer is not alive
            if state == True:#this means havn't sent it
                await send_group_at_all_msg(websocket,sunshine_group,f"{streamer} went offline")
                state = False#so send it and also change the state

async def serverRun(websocket,path):
    await mainfunc(websocket)

async def main():
    Set_Level()
    #sometimes i need to test new function,so i can set DEBUG mode
    #in this way,i send all my msg in my test group
    print("========================server main begin========================")
    server = await websockets.serve(serverRun, IP_ADDR, IP_PORT)
    await server.wait_closed()

asyncio.run(main())
