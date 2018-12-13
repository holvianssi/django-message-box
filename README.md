Django Message Box
==================

This project implements Inbox and Outbox models for reliable messaging
with Django.

The idea is that the sending side writes a message to database inside
the same database transaction where the event causing the message is
handled. Immediately after send there's an attempt to deliver the
message. If the attempt fails, there will be more attempts with
exponential backoff.

Outbox model
------------ 

First, you'll need to configure a transport for your messages in app
ready() handlers. A typical way to configure an Outbox transport is:
    Outbox.configure(
        'outbound_sct_payment',
        transport=HttpTransportTransport(
            to='https://receiver.com/api/inbox',
        )
    )

Now, to write and send a reliable message:

   Outbox.create_message(
       source='vault',
       type='outbound_sct_payment',
       payload={
           'text': 'Payload needs to be serializable to JSON'
       }
   )


This will save the message to database, and also schedule sending the
message.

Note that for transports it's extremely important that if the transport
returns success for send_message(), then the message is guaranteed to be
sent.

Finally, you need to configure resending. There are two ways to do that:

  1) Add task resend_unsent_messages to your celery periodic tasks config
  2) Use system's Cron to schedule the resending

The full list of changes to use the Outbox model with HttpTransport are:

  1) Include "outbox" in your INSTALLED_APPS
  2) Pick one of your existing apps, in ready() function configure a transport
     for a message type you want to handle.
  3) Configure a cron job or celery task for resending messages.
  4) Start creating messages!

Inbox model
----------- 

To use the Inbox model with HttpTransport you will need to do the following
changes:

  1) Include "inbox" in your INSTALLED_APPS
  2) Include inbox.urls in your urls.conf
  3) Configure a post_save handler for Inbox model (only handle the created case).
     From the post save handler launch the business logic.

Done!
