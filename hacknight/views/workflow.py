# -*- coding: utf-8- *-

from flask import g
from coaster.docflow import DocumentWorkflow, WorkflowState, WorkflowStateGroup
from hacknight.models.participant import Participant, ParticipantStatus
from hacknight.models.event import Event, EventStatus
from hacknight.views.login import lastuser

class ParticipantWorkflow(DocumentWorkflow):
    """
    workflow for participants
    """

    state_attr = 'status'
    pending = WorkflowState(ParticipantStatus.PENDING, title=u'pending', 
        description=u'State for participants who are interested, but waiting for event owner approval')
    waiting_list = WorkflowState(ParticipantStatus.WL, title=u'Waiting List', 
        description=u'State for participants who are interested but we dont have seats')
    confirmed = WorkflowState(ParticipantStatus.CONFIRMED, title=u'confirmed',
        description=u'State for participants who will attend hacknight')
    rejected = WorkflowState(ParticipantStatus.REJECTED, title=u'rejected', 
        description=u'State for participants who are rejected by event owner')
    withdrawn = WorkflowState(ParticipantStatus.WITHDRAWN, title=u'withdrawn', 
        description=u'State for participants who are uninterested due to several reason')
    #States how to become hacknight member
    #Yes it is very vague name, I need to comeup with very nice name
    path_to_hacknight = WorkflowStateGroup([pending, waiting_list], title=u'Path to hacknight', 
        description=u'If the participant is in any one of the state he/she can become hacknight member')
    reject_member = WorkflowStateGroup([pending, waiting_list], 
    title=u'Path to remove a member from to hacknight',
    description=u'If the participant is in any one of the state he/she can be rejected for hacknight') 
    withdrawn_member = WorkflowStateGroup([confirmed, waiting_list, pending], 
    title=u'Path to withdraw membership',
    description=u'If the participant is in any one of the state he/she can withdraw for hacknight')
    #copied from geekup, in hacknight only event owner can approve
    def permissions(self):
        """
            Permissions available to current user.
        """
        base_permissions = super(ParticipantWorkflow,self).permissions()
        raise
        base_permissions.append('participant')
        base_permissions.extend(lastuser.permissions())
        return base_permissions
    
    @waiting_list.transition(pending, 'owner', title=u'move to pending list', 
       description=u"Move to pending list, waiting for event owner approval",
       view="")
    def waiting_list_to_pending(self):
        pass
    
    @pending.transition(confirmed, 'owner', title=u'move to confirmed', 
       description=u"Move to confirmed from pending list with project owner or event owner approval", view="")
    def pending_to_confirm(self):
        pass

    @confirmed.transition(withdrawn, 'participant', title=u'withdrawn from confimed', 
       description=u"Withdraw from hacknight", view="withdraw_confirm")
    def withdraw_confirmed(self):
        self.document.status = ParticipantStatus.WITHDRAWN
 
    @pending.transition(withdrawn, 'participant', title=u'withdrawnfrom pending', 
       description=u"Withdraw from hacknight", view="withdraw_pending")
    def withdraw_pending(self):
        self.document.status = ParticipantStatus.WITHDRAWN

    @waiting_list.transition(withdrawn, 'participant', title=u'withdrawn from waiting', 
       description=u"Withdraw from hacknight", view="withdraw_waiting_list")
    def withdraw_waiting_list(self):
        self.document.status = ParticipantStatus.WITHDRAWN

    @rejected.transition(withdrawn, 'participant', title=u'withdrawn from waiting', 
       description=u"Withdraw from hacknight", view="withdraw_rejected")
    def withdraw_rejected(self):
        self.document.status = ParticipantStatus.WITHDRAWN


    def can_withdraw(self):
        return True if self.document.status is not ParticipantStatus.WITHDRAWN else False


ParticipantWorkflow.apply_on(Participant)
class EventWorkflow(DocumentWorkflow):

    """
    Workflow for Hacknight events.
    """

    state_attr = 'status'
    draft = WorkflowState(EventStatus.DRAFT, title=u"Draft")
    active = WorkflowState(EventStatus.ACTIVE, title=u"Active")
    closed = WorkflowState(EventStatus.CLOSED, title=u"Closed")
    completed = WorkflowState(EventStatus.COMPLETED, title=u"Completed")
    cancelled = WorkflowState(EventStatus.CANCELLED, title=u"Cancelled")
    rejected = WorkflowState(EventStatus.REJECTED, title=u"Rejected")
    withdrawn = WorkflowState(EventStatus.WITHDRAWN, title=u"Withdrawn")

     #: States in which an owner can edit
    editable = WorkflowStateGroup([draft, active], title=u"Editable")
    public = WorkflowStateGroup([active,closed],title=u"Public")
    openit = WorkflowStateGroup([draft],title=u"Open it")
    #: States in which a reviewer can view
    reviewable = WorkflowStateGroup([draft, active, closed, rejected, completed],
                                    title=u"Reviewable")


    def permissions(self):
        """
        Permissions available to current user.
        """
        base_permissions = super(EventWorkflow,
                                 self).permissions()
        if self.document.profile.userid == g.user.userid:
            base_permissions.append('owner')
        base_permissions.extend(lastuser.permissions())
        return base_permissions

    @draft.transition(active, 'owner', title=u"Open", category="primary",
        description=u"Open the Geekup for registrations.", view="event_open")
    def openit(self):
        """
        Open the Geekup.
        """
        if not self.document.status == EventStatus.PUBLISHED:
            self.document.status = EventStatus.PUBLISHED
    
    @draft.transition(cancelled, 'owner', title=u"Cancel", category="warning",
        description=u"Cancel the Geekup, before opening.", view="event_cancel" )
    def cancel(self):
        """
        Cancel the Geekup
        """
        pass

    @draft.transition(rejected, 'owner', title=u"Rejected", category="danger",
        description=u"Reject the Geekup proposed by someone else", view="event_reject")
    def reject(self):
        """
        Reject the Geekup
        """
        pass

    @draft.transition(withdrawn, 'owner', title=u"Withdraw", category="danger",
        description=u"Withdraw the Geekup",view="event_withdraw")
    def withdraw(self):
        """
        Withdraw the Geekup
        """
        pass

    @active.transition(closed, 'owner', title=u"Close", category="primary",
        description=u"Close registrations for the Geekup",view="event_close")
    def close(self):
        """
        Close the Geekup
        """
        pass


    @closed.transition(completed, 'owner',title=u"Complete", category="success",
        description=u"Geekup completed",view="event_completed")
    def complete(self):
        """
        Geekup is now completed.
        """
        pass


    def is_public(self):
        """
        Is the hacknight public?
        """
        if self.public():
            return True
        return False

    def can_view(self):
        """
        Can the current user view this?
        """
        permissions = self.permissions()
        if 'owner' in permissions:
            return True
        if 'reviewer' in permissions and self.reviewable():
            return True
        return False

    def can_edit(self):
        """
        Can the current user edit this?
        """
        return 'owner' in self.permissions() and self.editable()        

    def can_open(self):
        """
        Can the current user edit this?
        """
        return 'owner' in self.permissions() and self.openit()        
    def can_delete(self):
        """
        Can the current user edit this?
        """
        return 'owner' in self.permissions() and self.editable()        

EventWorkflow.apply_on(Event)
