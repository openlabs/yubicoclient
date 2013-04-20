YubiKey generates a One-Time Passcode (OTP) that your
application or service, ensuring that only users with 
a valid YubiKey can gain access. This api will help you 
to validate a OTP thus obtained against a yubico server. 
Also supports custom Yubikey validation servers in 
addition to the default Yubico servers.

Usage
=====

.. code-block:: python

    from yubicoclient import YubicoClient
    client = YubicoClient('<client id>', '<key>')
    client.verify('<OTP>')


Installation
============

    `pip install yubicoclient`


Useful Resources
================

  * `yubico <http://http://www.yubico.com/>`_
  * `Yubico Documentation <http://code.google.com/p/yubikey-val-server-php/wiki/ValidationProtocolV20>`_
  * `Source Code <https://github.com/openlabs/yubicoclient>`_


About Openlabs Technologies and Consulting Private Limited
##########################################################

Openlabs Technologies and Consulting Private Limited is a
global Information Technology and Management Consulting 
Company that helps small and medium businesses achieve high 
efficiency with cost effective business solutions. With 
customers and partners in four continents, Openlabs designs 
and delivers technology enabled innovative business solutions 
that addresses the needs of small and medium enterprises. 

Openlabs provides end to end solutions to businessess using 
a range of Free and Opensource Solutions (FOSS) Implemented 
by a team of highly skilled workforce comprising of domain 
and business experts.

The software division of Openlabs is a specialised division
of Rapid Application Development of business application with 
a proven expertise in OpenERP (and OpenObject). Tryton and
Django.

Technical Support
"""""""""""""""""

Phone: +1 813.793.6736 (USA)
Email: support@openlabs.co.in
Web: www.openlabs.co.in
