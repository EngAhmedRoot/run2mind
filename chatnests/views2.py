
class ChatnestsMessagesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        sender_id = request.GET.get('sender_id')

        if sender_id:
            messages = Chatnests_message.objects.filter(
                (Q(sender_id=sender_id) & Q(receiver=request.user)) | 
                (Q(sender_id=request.user) & Q(receiver_id=sender_id))
            ).select_related('sender').order_by('timestamp')

            for message in messages:
                sender = message.sender
                message.sender_name = self.get_sender_name(sender)
                message.sender_avatar = sender.file
                message.room_name = self.get_room_name(sender.id, request.user.id)

            return render(request, 'chatnests/chatnests_messages.html', {'messages': messages})

        latest_messages = (
            Chatnests_message.objects.filter(receiver=self.request.user)
            .values('sender')
            .annotate(latest_timestamp=Max('timestamp'))
        )

        messages = Chatnests_message.objects.filter(
            Q(receiver=self.request.user) & 
            Q(timestamp__in=[item['latest_timestamp'] for item in latest_messages])
        ).select_related('sender').order_by('-timestamp')

        for message in messages:
            sender = message.sender
            message.sender_name = self.get_sender_name(sender)
            message.sender_avatar = sender.file
            message.room_name = self.get_room_name(sender.id, request.user.id)

        return render(request, 'chatnests/chatnests_messages.html', {'messages': messages})

    def post(self, request, *args, **kwargs):
        sender_id = request.POST.get('sender_id')
        print(f"your sender_id is: {sender_id}")

        receiver_id = request.POST.get('receiver_id')
        print(f"your receiver_id is: {receiver_id}")

        if sender_id:
            messages  = Chatnests_message.objects.filter((Q(sender_id=sender_id, receiver=request.user) | Q(sender=request.user, receiver_id=sender_id))).select_related('sender').order_by('timestamp')
            print(f"Messages fetched: {messages.count()}")

            messages.update(is_read=1)

            for message in messages:
                sender = message.sender
                message.sender_name = self.get_sender_name(sender)
                message.sender_avatar = self.get_sender_avatar(sender)
                message.room_name = self.get_room_name(sender.id, request.user.id)
                print(f"Message {message.id} - Sender: {message.sender_name}, Content: {message.content}, Room Name: {message.room_name}")



            return JsonResponse({
                'html': render_to_string('chatnests/_chatnests_messages_partial.html', {'messages_private': messages}, request=request),'message_count': messages.count()
            })


        message_content = request.POST.get('content')
        receiver_id = request.POST.get('receiver_id')

        print(f"Message content: {message_content}, Your Receiver ID will be: {receiver_id}")


        if message_content and receiver_id:
            receiver = get_object_or_404(Customusers, id=receiver_id)
            sender = request.user
            #print(f"Receiver is k to: {receiver}")
            #print(f"Sender is k to: {sender}")

            new_message = Chatnests_message.objects.create(
                content=message_content,
                sender=sender,
                receiver=receiver
            )

            print(f"New message created: {new_message.content}")

            room_name = self.get_room_name(sender.id, receiver.id)

            return JsonResponse({
                'message': 'Message sent successfully!',
                'sender_id': sender.id,
                'sender_name': self.get_sender_name(sender),
                'sender_avatar': self.get_sender_avatar(sender),
                'message_content': new_message.content,
                'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'room_name': room_name
            }, status=200)

        return JsonResponse({'error': 'Invalid sender or receiver ID'}, status=400)



    def get_sender_name(self, sender):
        return f"{sender.first_name} {sender.last_name}"


    def get_sender_avatar(self, sender):
        if hasattr(sender, 'file') and bool(sender.file):
            return sender.file.url 
        return None

    def get_room_name(self, sender_id, receiver_id):
        return f"chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
