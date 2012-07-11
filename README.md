This is a simple web interface written in web2py we use at Bullard ISD to track users who come into the library. There is a frontend where users just log into a web interface (using https://github.com/korylprince/WebKiosk) and a backend where teachers and other staff can view statistics to see who has logged in and when.

pyLibraryTracker
https://github.com/korylprince/pyLibraryTracker

#Installing#

Simply add the application folder to your web2py application folder.

You will have to edit the authentication settings in controllers check.py and default.py.

check.py controls logins for the teacher side (so you might want to only allow one group), and default.py controls logins for the frontend side (so you'll probably want to allow everyone.)

You will also have to edit the authentication settings in the model db.py in the findUserAttr function.

By default, the user\_type attribute comes from the user's parent OU name.

If a users type is a year, then it will automatically be shown as their grade level (Senior, Freshman, 2nd, etc...)

This can be changed in the model db.py.

To use Active Directory with allowed groups, currently web2py must be patched.
Please see http://www.web2pyslices.com/slice/show/1493/active-directory-ldap-with-allowed-groups on how to set that up.
This issue has been fixed in a new development version of web2py.

If you have any issues or questions, email the email address below, or open an issue at:
https://github.com/korylprince/pyLibraryTracker/issues

#Usage#

Usage is fairly straightforward. Visit https://yoursite/yourappname/ for the frontend. Visit https://yoursite/yourappname/check/ for the teacher side. The teacher side can search by Name, Start Date, End Date, and User Type.

The result is displayed in a table of all logins, as well as a [jqplot](http://www.jqplot.com/) chart plotting out logins.

#Copyright Information#

Some of the css and javascript files have their own third-party licenses.

All other code is Copyright 2012 Kory Prince (korylprince at gmail dot com.) This code is licensed under the GPL v3 which is included in this distribution. If you'd like it licensed under another license then send me an email.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
