Django Message Box
==================

This project implements Inbox and Outbox models for reliable messaging
with Django.

The full list of changes to use the Outbox model with HttpTransport are:

  1) Include "outbox" in your INSTALLED_APPS, run migrations
  2) Pick one of your existing apps, in ready() function register a transport
     for a message type you want to handle.
  3) Configure a cron job or celery task for resending messages.
  4) Start creating messages!

To use the Inbox model with HttpTransport you will need to do the following
changes:

  1) Include "inbox" in your INSTALLED_APPS, run migrations
  2) Include inbox.urls in your urls.conf
  3) Add a handler using inbox service .register_handler() method.
     The handler is a callable accepting message as sole argument.

The way the Outbox model works is that the message is saved to the database when
create_message() is called. When the message has been premanently persisted to
the DB, a transport configured for the message will deliver the message to
the wanted recipient. In case there's failures retry will happen automatically.
Finally, Inbox will guarantee one message is received at most once.

Example changes in commits https://github.com/holvi/vault/commit/a6d461f12bcc5ae6d80c165998ba5a062d0238fc
and https://github.com/holvi/lexoffice/commit/8f1b4db1fb75f63bdf8611490a24e1a761387cb4

Outbox in detail
----------------

First, you'll need to configure a transport for your messages in app
ready() handlers. A typical way to configure an Outbox transport is:

    from messagebox.outbox import get_outbox_service
    service = get_outbox_service()
    service.register_transport(
        message_type='outbound_sct_payment',
        transport=HttpTransportTransport(
            to='https://receiver.com/api/inbox',
        )
    )

Now, to write and send a reliable message:

    service.create_message(
        message_source='vault',
        message_type='outbound_sct_payment',
        payload={
            'text': 'Payload needs to be serializable to JSON'
        }
    )

This will save the message to database, and also schedule sending the
message.

Finally, you need to configure resending, this can be done by adding
task resend_outbox_messages to your celery periodic tasks config:

     'resend_outbox_messages': {
         'task': 'outbox.tasks.resend_unsent_messages',
         'schedule': timedelta(seconds=30),
     }


Inbox in detail
---------------

There's two changes you need to implement on receiving side
to start receiving messages:

   1. Add inbox to INSTALLED_APPS, run migrations
   2. Add inbox urls to your URLS config, for example:
      url(r'^api/', include('inbox.urls'))
      This is only needed if you want to receive messages
      using HTTP.

Now you are ready to start receiving messages. For any
message received, you'll need to configure a handler.
The best place to do this is in your App.ready() function:

    from messagebox.inbox import get_inbox_service
    get_inbox_service().register_handler(
        'vault', 'payment_executed', handler_accepting_message_as_param
    )

Done, now you have reliable message passing implementation in
place!
