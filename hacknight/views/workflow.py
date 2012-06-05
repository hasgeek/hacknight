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
    pending = WorkflowState(ParticipantStatus.PENDING, title=u'pending', description=u'State for participants who are interested, but waiting for event manager approval')
    waiting_list = WorkflowState(ParticipantStatus.WL, title=u'Waiting List', description=u'State for participants who are interested but we dont have seats')
    confirmed = WorkflowState(ParticipantStatus.CONFIRMED, title=u'confirmed', description=u'State for participants who will attend hacknight')
    rejected = WorkflowState(ParticipantStatus.REJECTED, title=u'rejected', description=u'State for participants who are rejected by event manager')
    withdrawn = WorkflowState(ParticipantStatus.WITHDRAWN, title=u'withdrawn', description=u'State for participants who are uninterested due to several reason')

    

