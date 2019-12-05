# -*- coding: utf-8- *-

from flask import g
from coaster.docflow import DocumentWorkflow, WorkflowState, WorkflowStateGroup
from hacknight.models.participant import Participant, PARTICIPANT_STATUS
from hacknight.models.event import Event, EVENT_STATUS
from hacknight.views.login import lastuser


class ParticipantWorkflow(DocumentWorkflow):
    """
    workflow for participants
    """

    state_attr = 'status'
    pending = WorkflowState(PARTICIPANT_STATUS.PENDING, title='Pending list',
        description='State for participants who are interested, but waiting for event owner approval')
    waiting_list = WorkflowState(PARTICIPANT_STATUS.WL, title='Waiting list',
        description='State for participants who are interested but we dont have seats')
    confirmed = WorkflowState(PARTICIPANT_STATUS.CONFIRMED, title='Confirmed list',
        description='State for participants who will attend hacknight')
    rejected = WorkflowState(PARTICIPANT_STATUS.REJECTED, title='Rejected list',
        description='State for participants who are rejected by event owner')
    withdrawn = WorkflowState(PARTICIPANT_STATUS.WITHDRAWN, title='Withdrawn list',
        description='State for participants who are uninterested due to several reason')
    attended = WorkflowState(PARTICIPANT_STATUS.ATTENDED, title='Attended list',
        description='State for confirmed participants who attended hacknight')
    #States how to become hacknight member
    #Yes it is very vague name, I need to comeup with very nice name
    path_to_hacknight = WorkflowStateGroup([pending, waiting_list], title='Path to hacknight',
        description='If the participant is in any one of the state he/she can become hacknight member')
    reject_member = WorkflowStateGroup([pending, waiting_list],
    title='Path to remove a member from to hacknight',
    description='If the participant is in any one of the state he/she can be rejected for hacknight')
    withdrawn_member = WorkflowStateGroup([confirmed, waiting_list, pending],
    title='Path to withdraw membership',
    description='If the participant is in any one of the state he/she can withdraw for hacknight')
    #copied from geekup, in hacknight only event owner can approve

    def permissions(self):
        """
            Permissions available to current user.
        """
        base_permissions = super(ParticipantWorkflow, self).permissions()
        # raise
        base_permissions.add('participant')
        base_permissions.update(lastuser.permissions())
        return base_permissions

    @waiting_list.transition(pending, 'owner', title='move to pending list',
       description="Move to pending list, waiting for event owner approval",
       view="")
    def waiting_list_to_pending(self):
        pass

    @pending.transition(confirmed, 'owner', title='move to confirmed',
       description="Move to confirmed from pending list with project owner or event owner approval", view="")
    def pending_to_confirm(self):
        pass

    @confirmed.transition(withdrawn, 'participant', title='withdrawn from confirmed',
       description="Withdraw from hacknight", view="withdraw_confirm")
    def withdraw_confirmed(self):
        self.document.status = PARTICIPANT_STATUS.WITHDRAWN
        
    @confirmed.transition(attended, 'participant', title='confirmed participants who attended hacknight',
       description="Attended hacknight", view="attend_confirmed")
    def attend_confirmed(self):
        self.document.status = PARTICIPANT_STATUS.ATTENDED

    @pending.transition(withdrawn, 'participant', title='withdrawnfrom pending',
       description="Withdraw from hacknight", view="withdraw_pending")
    def withdraw_pending(self):
        self.document.status = PARTICIPANT_STATUS.WITHDRAWN

    @waiting_list.transition(withdrawn, 'participant', title='withdrawn from waiting',
       description="Withdraw from hacknight", view="withdraw_waiting_list")
    def withdraw_waiting_list(self):
        self.document.status = PARTICIPANT_STATUS.WITHDRAWN

    @rejected.transition(withdrawn, 'participant', title='withdrawn from waiting',
       description="Withdraw from hacknight", view="withdraw_rejected")
    def withdraw_rejected(self):
        self.document.status = PARTICIPANT_STATUS.WITHDRAWN

    def can_withdraw(self):
        return True if self.document.status is not PARTICIPANT_STATUS.WITHDRAWN else False

ParticipantWorkflow.apply_on(Participant)


class EventWorkflow(DocumentWorkflow):

    """
    Workflow for Hacknight events.
    """

    state_attr = 'status'
    draft = WorkflowState(EVENT_STATUS.DRAFT, title="Draft")
    active = WorkflowState(EVENT_STATUS.ACTIVE, title="Active")
    closed = WorkflowState(EVENT_STATUS.CLOSED, title="Closed")
    completed = WorkflowState(EVENT_STATUS.COMPLETED, title="Completed")
    cancelled = WorkflowState(EVENT_STATUS.CANCELLED, title="Cancelled")
    rejected = WorkflowState(EVENT_STATUS.REJECTED, title="Rejected")
    withdrawn = WorkflowState(EVENT_STATUS.WITHDRAWN, title="Withdrawn")
    published = WorkflowState(EVENT_STATUS.PUBLISHED, title="Public")
    unlisted = WorkflowState(EVENT_STATUS.UNLISTED, title="Unlisted")

     #: States in which an owner can edit
    editable = WorkflowStateGroup([draft, active, closed, completed, cancelled, rejected, withdrawn, published, unlisted], title="Editable")
    public = WorkflowStateGroup([active, closed], title="Public")
    appliable = WorkflowStateGroup([active, published, unlisted], title="User can apply for an event")
    openit = WorkflowStateGroup([draft], title="Open it")
    #: States in which a reviewer can view
    reviewable = WorkflowStateGroup([draft, active, closed, rejected, completed],
                                    title="Reviewable")

    def permissions(self):
        """
        Permissions available to current user.
        """
        base_permissions = super(EventWorkflow,
                                 self).permissions()
        if self.document.owner_is(g.user):
            base_permissions.add('owner')
        base_permissions.update(lastuser.permissions())
        return base_permissions

    @draft.transition(active, 'owner', title="Open", category="primary",
        description="Open the hacknight for registrations.", view="event_open")
    def openit(self):
        """
        Open the hacknight.
        """
        if not self.document.status == EVENT_STATUS.PUBLISHED:
            self.document.status = EVENT_STATUS.PUBLISHED

    @draft.transition(cancelled, 'owner', title="Cancel", category="warning",
        description="Cancel the hacknight, before opening.", view="event_cancel")
    def cancel_draft(self):
        """
        Cancel the hacknight
        """
        self.document.status = EVENT_STATUS.CANCELLED

    @active.transition(cancelled, 'owner', title="Cancel", category="warning",
        description="Cancel the hacknight, before opening.", view="event_cancel")
    def cancel_active(self):
        """
        Cancel the hacknight
        """
        self.document.status = EVENT_STATUS.CANCELLED

    @draft.transition(rejected, 'owner', title="Rejected", category="danger",
        description="Reject the hacknight proposed by someone else", view="event_reject")
    def reject(self):
        """
        Reject the hacknight
        """
        pass

    @draft.transition(withdrawn, 'owner', title="Withdraw", category="danger",
        description="Withdraw the hacknight", view="event_withdraw")
    def withdraw(self):
        """
        Withdraw the hacknight
        """
        pass

    @active.transition(closed, 'owner', title="Close", category="primary",
        description="Close registrations for the hacknight", view="event_close")
    def close(self):
        """
        Close the hacknight
        """
        pass

    @closed.transition(completed, 'owner', title="Complete", category="success",
        description="hacknight completed", view="event_completed")
    def complete(self):
        """
        Hacknight is now completed.
        """
        pass

    def is_public(self):
        """
        Is the hacknight public?
        """
        return self.public()

    def can_view(self):
        """
        Can the current user view this?
        """
        return self.public() or 'owner' in self.permissions()

    def can_edit(self):
        """
        Can the current user edit this?
        """
        return 'owner' in self.permissions() and self.editable()

    def can_open(self):
        """
        Can the current user edit this?
        """
        return 'owner' in self.permissions()

    def can_delete(self):
        """
        Can the current user edit this?
        """
        return 'owner' in self.permissions() and self.editable()

    def can_apply(self):
        return self.appliable()

EventWorkflow.apply_on(Event)
