from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import json

def new_msg(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    chat = Chat.objects.filter(users__in=[body['msgFrom'], body['msgTo']])
    for x in chat.all():
        if x.id != request.user.id:
            chat = False

    if chat:
        print('chat found')
        Message.objects.create(chat_id=chat[0].id, user_id=body['msgFrom'], message=body['msg'])
    else:
        print('chat not found')
        newChat = Chat.objects.create()
        newChat.users.add(body['msgFrom'], body['msgTo'])
        # if int(body['msgFrom']) == request.user.id:
        #     newChat.lastMessageOwn = True
        #     newChat.save()
        newChat.lastMsgBy_id = request.user.id
        newChat.save()
        Message.objects.create(chat=newChat, user_id=body['msgFrom'], message=body['msg'])
    # Message.objects.create(messageTo_id=body['msgTo'],messageFrom_id=body['msgFrom'],message=body['msg'])
    return JsonResponse({'foo': 'bar'})



def get_msg(request):
    return_dict = {}
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    chat = Chat.objects.get(id=body['chat_id'])

    if not chat.lastMsgBy == request.user:
        chat.isNewMessages = False
        chat.save()
    userInfo ={}
    chatMsg = []
    for user in chat.users.all():
        if user.id != request.user.id:
            user_qs = User.objects.get(id=user.id)
            user_name = user_qs.name
            user_avatar = user_qs.get_avatar
            userInfo = {
                'user_name': user_name,
                'user_avatar': user_avatar,

            }
    for x in chat.message_set.all():
        chatItem = {}
        chatItemInner = []
        if not x.user == request.user:
            x.isUnread = False
            x.save()
        if x.user == request.user:
            chatItem['own']=[x.message,x.createdAt.strftime("%d.%m.%Y,%H:%M:%S")]
        else:
            chatItem['from'] = [x.message,x.createdAt.strftime("%d.%m.%Y,%H:%M:%S")]
        chatMsg.append(chatItem)
    return_dict['userInfo'] = userInfo
    return_dict['chatMsg'] = chatMsg
    return JsonResponse(return_dict,safe=False)


def add_msg(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    Message.objects.create(chat_id=body['chatId'], user_id=body['msgFrom'], message=body['msg'])
    # if int(body['msgFrom']) == request.user.id:
    #     chat_qs = Chat.objects.get(id=int(body['chatId']))
    #     chat_qs.lastMessageOwn = True
    #     chat_qs.save()
    chat_qs = Chat.objects.get(id=int(body['chatId']))
    chat_qs.lastMsgBy_id = request.user.id
    chat_qs.save()
    return JsonResponse('ok',safe=False)


def get_chats(request):
    return_dict = {}
    allChats = Chat.objects.filter(users__in=[request.user.id])
    allUnreadChats = allChats.filter(isNewMessages=True)
    for x in allUnreadChats:
        if x.message_set.last().user == request.user:
            print('last msg is own')
            print(x.pk)

            allUnreadChats = allUnreadChats.exclude(pk=x.pk)
    allReadChats = allChats.all()

    print('allUnreadChats', allUnreadChats)
    print('allReadChats', allReadChats)
    unreadChats = []
    readChats = []
    for chat in allUnreadChats:
        user_name = ''
        user_avatar = ''
        for user in chat.users.all():
            if user.id != request.user.id:
                user_qs = User.objects.get(id=user.id)
                user_name = user_qs.name
                user_avatar = user_qs.get_avatar

        unreadChats.append({
            'chat_id': chat.id,
            'chat_from': user_name,
            'user_avatar': user_avatar,
            'unread_mgs_count': len(chat.message_set.all().filter(isUnread=True)),
            'last_msg': chat.message_set.last().message,
            'last_msg_time': chat.message_set.last().createdAt.strftime("%d.%m.%Y,%H:%M:%S")
        })
    for chat in allReadChats:
        user_name = ''
        user_avatar = ''
        for user in chat.users.all():
            if user.id != request.user.id:
                user_qs = User.objects.get(id=user.id)
                user_name = user_qs.name
                user_avatar = user_qs.get_avatar

        readChats.append({
            'chat_id': chat.id,
            'chat_from': user_name,
            'user_avatar': user_avatar,
            'unread_mgs_count': len(chat.message_set.all().filter(isUnread=True)),
            'last_msg': chat.message_set.last().message,
            'last_msg_time': chat.message_set.last().createdAt.strftime("%d.%m.%Y,%H:%M:%S")
        })
    print(unreadChats)
    return_dict['unreadChats']=unreadChats
    return_dict['readChats'] = readChats
    return JsonResponse(return_dict)