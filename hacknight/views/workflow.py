# -*- coding: utf-8 -*-

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
    pending = WorkflowState(PARTICIPANT_STATUS.PENDING, title=u'Pending list',
        description=u'State for participants who are interested, but waiting for event owner approval')
    waiting_list = WorkflowState(PARTICIPANT_STATUS.WL, title=u'Waiting list',
        description=u'State for participants who are interested but we dont have seats')
    confirmed = WorkflowState(PARTICIPANT_STATUS.CONFIRMED, title=u'Confirmed list',
        description=u'State for participants who will attend hacknight')
    rejected = WorkflowState(PARTICIPANT_STATUS.REJECTED, title=u'Rejected list',
        description=u'State for participants who are rejected by event owner')
    withdrawn = WorkflowState(PARTICIPANT_STATUS.WITHDRAWN, title=u'Withdrawn list',
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
        base_permissions = super(ParticipantWorkflow, self).permissions()
        # raise
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
        self.document.status = PARTICIPANT_STATUS.WITHDRAWN

    @pending.transition(withdrawn, 'participant', title=u'withdrawnfrom pending',
       description=u"Withdraw from hacknight", view="withdraw_pending")
    def withdraw_pending(self):
        self.document.status = PARTICIPANT_STATUS.WITHDRAWN

    @waiting_list.transition(withdrawn, 'participant', title=u'withdrawn from waiting',
       description=u"Withdraw from hacknight", view="withdraw_waiting_list")
    def withdraw_waiting_list(self):
        self.document.status = PARTICIPANT_STATUS.WITHDRAWN

    @rejected.transition(withdrawn, 'participant', title=u'withdrawn from waiting',
       description=u"Withdraw from hacknight", view="withdraw_rejected")
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
    draft = WorkflowState(EVENT_STATUS.DRAFT, title=u"Draft")
    active = WorkflowState(EVENT_STATUS.ACTIVE, title=u"Active")
    closed = WorkflowState(EVENT_STATUS.CLOSED, title=u"Closed")
    completed = WorkflowState(EVENT_STATUS.COMPLETED, title=u"Completed")
    cancelled = WorkflowState(EVENT_STATUS.CANCELLED, title=u"Cancelled")
    rejected = WorkflowState(EVENT_STATUS.REJECTED, title=u"Rejected")
    withdrawn = WorkflowState(EVENT_STATUS.WITHDRAWN, title=u"Withdrawn")
    published = WorkflowState(EVENT_STATUS.PUBLISHED, title="Published")

    #: States in which an owner can edit
    editable = WorkflowStateGroup([draft, active, published, closed], title=u"Editable")
    public = WorkflowStateGroup([published, closed], title=u"Public")
    appliable = WorkflowStateGroup([active, published], title="User can apply for an event")

    openit = WorkflowStateGroup([draft], title=u"Open it")
    create_projects = WorkflowStateGroup([draft, active, published], title="States in which projects can be created")
    #: States in which a reviewer can view
    reviewable = WorkflowStateGroup([draft, published],
                                    title=u"Reviewable")

    def permissions(self):
        """
        Permissions available to current user.
        """
        base_permissions = super(EventWorkflow,
                                 self).permissions()
        if self.document.owner_is(g.user):
            base_permissions.append('owner')
        base_permissions.extend(lastuser.permissions())
        return base_permissions

    @draft.transition(published, 'owner', title=u"Open", category="primary",
        description=u"Make hacknight public", view="event_change")
    def openit(self):
        """
        Open the hacknight.
        """
        if not self.document.status == EVENT_STATUS.PUBLISHED:
            self.document.status = EVENT_STATUS.PUBLISHED

    @draft.transition(cancelled, 'owner', title=u"Cancel", category="warning",
        description=u"Cancel hacknight", view="event_change")
    def cancel_draft(self):
        """
        Cancel the hacknight
        """
        self.document.status = EVENT_STATUS.CANCELLED

    @active.transition(cancelled, 'owner', title=u"Cancel", category="warning",
        description=u"Cancel hacknight", view="event_change")
    def cancel_active(self):
        """
        Cancel the hacknight
        """
        self.document.status = EVENT_STATUS.CANCELLED

    @active.transition(closed, 'owner', title=u"Close", category="primary",
        description=u"Close registrations", view="event_change")
    def close(self):
        """
        Close the hacknight
        """
        self.document.status = EVENT_STATUS.CLOSED


    @published.transition(cancelled, 'owner', title=u"Cancel", category="warning",
        description=u"Cancel hacknight", view="event_change")
    def deactive(self):
        """
        Cancel the hacknight
        """
        self.document.status = EVENT_STATUS.CANCELLED

    @published.transition(closed, 'owner', title=u"Close", category="primary",
        description=u"Close registration", view="event_change")
    def published_close(self):
        """
        Close the hacknight
        """
        self.document.status = EVENT_STATUS.CLOSED

    @closed.transition(active, 'owner', title=u"Complete", category="success",
        description=u"Reopen hacknight", view="event_change")
    def reopen(self):
        """
        Hacknight is now completed.
        """
        self.document.status = EVENT_STATUS.ACTIVE

    @cancelled.transition(active, 'owner', title=u"Complete", category="success",
        description=u"Reopen hacknight", view="event_change")
    def cancel_reopen(self):
        """
        Hacknight is now completed.
        """
        self.document.status = EVENT_STATUS.ACTIVE

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

    def is_active(self):
        return self.create_projects()

    def can_apply(self):
        return self.appliable()


EventWorkflow.apply_on(Event)
