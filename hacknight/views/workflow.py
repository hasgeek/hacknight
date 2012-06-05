# -*- coding: utf-8- *-

from flask import g
from coaster.docflow import DocumentWorkflow, WorkflowState, WorkflowStateGroup
from hacknight.models.participant import Participant, ParticipantStatus
from hacknight,views.login import lastuser

class ParticipantWorkFlow(DocumentWorkflow):
    """
    workflow for participants
    """

    state_attr = 'status'
    pending = WorkflowState(ParticipantStatus.PENDING, title=u'pending', 
        description=u'State for participants who are interested, 
                    but waiting for event manager approval')
    waiting_list = WorkflowState(ParticipantStatus.WL, title=u'Waiting List', 
        description=u'State for participants who are interested 
                      but we dont have seats')
    confirmed = WorkflowState(ParticipantStatus.CONFIRMED, title=u'confirmed',
        description=u'State for participants who will attend hacknight')
    rejected = WorkflowState(ParticipantStatus.REJECTED, title=u'rejected', 
        description=u'State for participants who are rejected by event manager')
    withdrawn = WorkflowState(ParticipantStatus.WITHDRAWN, title=u'withdrawn', 
        description=u'State for participants who are uninterested due to 
                      several reason')
   
   #States how to become hacknight member
   #Yes it is very vague name, I need to comeup with very nice name
   path_to_hacknight = WorkflowStateGroup([pending, waiting_list], title=u'Path 
        to hacknight', description=u'If the participant is in any one of the 
        state he/she can become hacknight member')

   #copied from geekup, in hacknight only event manager or site admin can approve
   def permissions(self):
       """
           Permissions available to current user.
       """
       base_permissions = super(EventWorkflow,self).permissions()
       if self.document.user == g.user:
           base_permissions.append('manager')
           base_permissions.extend(lastuser.permissions())
       elif lastuser.has_permission('siteadmin'):
           base_permissions.append('siteadmin')
           base_permissions.extend(lastuser.permissions())
       return base_permissions
    
   @waiting_list.transition(pending, 'manager', title=u'move to pending list', 
       description=u"Move to pending list, waiting for event manager approval",
       view="")
   def waiting_list_to_pending(self):
       pass


