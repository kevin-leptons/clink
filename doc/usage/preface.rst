Preface
=======

Before dick in details into Clink, you should know "What is Clink?".
After that, you get Clink's advantage and disadvantage then use Clink
in effective way. This section help you get it.

Clink is HTTP API library. HTTP is big, large, huge domain and Clink
doesn't try to work in all of concepts, it focuses to build HTTP APIs
to get, process and save data. If you want something which help you build
web front-end application, then go back, Clink is back-end side.

Although Clink focus on HTTP APIs, it also contains many concepts rather than
HTTP API such as Application Architecture, Database Model, Authentication,
Authorization, and so on. It provides best model to work immediately.
That way reduces knowledge which developers must to know in details to help
them focus on logic of application. In simple, you can write first logic
code lines after you install Clink and don't worry about Routing,
Authentication, etc.

Clink likes extensibility than customizable. You can see that if you look
into Clink's built-in module, it limits option arguments, it is short, clean
and do one thing as best as possible. In case you aren't comfort with
it's behaviors, functions, etc, that time you write new module instead
try to custom it.

It doesn't meant that you can custom any things in Clink. For example,
clink.service.auth.AuthConf defines 4 hours for token life, 30 days for
refresh token life in default, but you still can use your values.

Clink written in Python and Python runs on cross platform but Clink run
on Unix-like platform. Because Clink is server side library, it need to 
work as well as possible on server side, when Unix-like is best choice for
server side. Most popular Unix-like platform for server side is 
operating system base on Linux kernel such as Debian, CentOS, etc...

Now, if you agreed with our terms: **HTTP API**, **Backend Programming**,
**Extensibility instead of Customizable**, **Unix-like Platform**, 
then inspect Clink.
