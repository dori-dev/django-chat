"""chat test
"""
from datetime import datetime
from django.db import IntegrityError
from django.test import TestCase
from .models import Message, Chat, User


class MessageTestCase(TestCase):
    """test Message model
    """

    def setUp(self):
        self.test_user1 = User.objects.create(username="john")
        self.test_user2 = User.objects.create(username="alice")
        chat: Chat = Chat.objects.create(name="chat_room1")
        chat.members.add(self.test_user1)
        self.test_room1 = chat
        chat: Chat = Chat.objects.create(name="chat_room2")
        chat.members.add(self.test_user1)
        chat.members.add(self.test_user2)
        self.test_room2 = chat

    def test_message_user(self):
        message: Message = Message.objects.create(
            author=self.test_user2,
            content="test",
            room=self.test_room2)
        self.assertEqual(message.author.username, "alice")

    def test_message_content(self):
        message: Message = Message.objects.create(
            author=self.test_user1,
            content="12345678",
            room=self.test_room2)
        self.assertEqual(message.content, "12345678")

    def test_message_length(self):
        message: Message = Message.objects.create(
            author=self.test_user1,
            content="ali",
            room=self.test_room1)
        self.assertEqual(len(message.content), 3)

    def test_message_no_user(self):
        with self.assertRaises(IntegrityError):
            Message.objects.create(
                author=None, content="test", room=self.test_room2)

    def test_message_create_retrieve(self):
        message_id = Message.objects.create(
            author=self.test_user1,
            content="the content",
            room=self.test_room2).id
        message: Message = Message.objects.get(id=message_id)
        # Asserts
        self.assertEqual(message.content, "the content")
        self.assertEqual(message.author, self.test_user1)
        self.assertEqual(message.room, self.test_room2)
        self.assertEqual(message.room.name, "chat_room2")

    def test_author_username(self):
        message: Message = Message.objects.create(
            author=self.test_user2,
            content="hello there",
            room=self.test_room2)
        self.assertEqual(message.author_username(), "alice")

    def test_get_time(self):
        current_time = datetime.now()
        formated_time = datetime.strftime(
            current_time,
            "%I:%M %p")
        message: Message = Message.objects.create(
            author=self.test_user1,
            content="this is for test time :)",
            room=self.test_room1)
        self.assertEqual(message.get_time(), formated_time)


class ChatTestCase(TestCase):
    """test Chat model
    """

    def setUp(self):
        self.test_user1 = User.objects.create(username="John")
        self.test_user2 = User.objects.create(username="Alice")
        self.test_user3 = User.objects.create(username="Bill")
        self.test_user4 = User.objects.create(username="Rose")

    def test_chat_member(self):
        chat: Chat = Chat.objects.create(name="greeting")
        chat.members.add(self.test_user1)
        self.assertEqual(chat.members.count(), 1)

    def test_chat_members(self):
        chat: Chat = Chat.objects.create(name="greeting")
        chat.members.add(self.test_user1)
        chat.members.add(self.test_user2)
        self.assertEqual(chat.members.count(), 2)

    def test_twice_chat_members(self):
        chat: Chat = Chat.objects.create(name="greeting")
        chat.members.add(self.test_user1)
        chat.members.add(self.test_user1)
        self.assertEqual(chat.members.count(), 1)

    def test_chat_empty_member(self):
        chat: Chat = Chat.objects.create(name="greeting")
        self.assertEqual(chat.members.count(), 0)

    def test_chat_name(self):
        chat: Chat = Chat.objects.create(name="Hi-There")
        self.assertEqual(chat.name, "Hi-There")

    def test_chat_empty_name(self):
        chat: Chat = Chat.objects.create()
        self.assertEqual(chat.name, "welcome")

    def test_all_group(self):
        Chat.objects.create(name="group-1")
        Chat.objects.create(name="listener")
        Chat.objects.create(name="group-3")
        Chat.objects.create(name="group-2")
        self.assertEqual(
            Chat.all_groups(), ["group-2", "group-3", "group-1"])
        self.assertEqual(len(Chat.all_groups()), 3)

    def test_members_list(self):
        chat: Chat = Chat.objects.create(name="family")
        chat.members.add(self.test_user1)
        chat.members.add(self.test_user2)
        chat.members.add(self.test_user4)
        chat.members.add(self.test_user3)
        members = Chat.get_members_list(chat.room_id)
        self.assertEqual(len(members), 4)

    def test_user_empty_group(self):
        me = self.test_user3
        chat1: Chat = Chat.objects.create(name="saved")
        chat1.members.add(me)
        chat2: Chat = Chat.objects.create(name="test")
        chat2.members.add(me)
        chat3: Chat = Chat.objects.create(name="hello")
        chat3.members.add(me)
        groups = Chat.your_group(me)
        self.assertEqual(groups, [])

    def test_user_groups(self):
        me = self.test_user2
        chat1: Chat = Chat.objects.create(name="welcome")
        chat1.members.add(me)
        chat2: Chat = Chat.objects.create(name="nice")
        chat2.members.add(me)
        chat3: Chat = Chat.objects.create(name="hello")
        chat3.members.add(me)
        Message.objects.create(
            author=me,
            content="hello there",
            room=chat2
        )
        Message.objects.create(
            author=me,
            content="i am join you!!",
            room=chat1
        )
        groups = Chat.your_group(me)
        self.assertEqual(groups, ["welcome", "nice"])
