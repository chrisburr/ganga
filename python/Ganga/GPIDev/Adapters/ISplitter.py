##########################################################################
# Ganga Project. http://cern.ch/ganga
#
# $Id: ISplitter.py,v 1.1 2008-07-17 16:40:52 moscicki Exp $
##########################################################################

from Ganga.Core.exceptions import SplitterError
from Ganga.GPIDev.Base import GangaObject
from Ganga.GPIDev.Base.Proxy import TypeMismatchError, isType, stripProxy
from Ganga.GPIDev.Schema import Schema, Version
from Ganga.Utility.util import containsGangaObjects


class ISplitter(GangaObject):

    """
    """
    _schema = Schema(Version(0, 0), {})
    _category = 'splitters'
    _hidden = 1

    def createSubjob(self, job, additional_skip_args=None):
        """ Create a new subjob by copying the master job and setting all fields correctly.
        """
        from Ganga.GPIDev.Lib.Job import Job
        if additional_skip_args is None:
            additional_skip_args = []

        j = Job()
        skipping_args = ['splitter', 'inputsandbox', 'inputfiles', 'inputdata', 'subjobs']
        for arg in additional_skip_args:
            skipping_args.append(arg)
        j.copyFrom(job, skipping_args)
        j.splitter = None
        j.inputsandbox = []
        j.inputfiles = []
        j.inputdata = []
        return j

    def split(self, job):
        """ Return a list of subjobs generated from a master job.  The
        original  master  job should  not  be  modified.  This  method
        should be implemented in the derived classes.

        Splitter  changes certain  parts of  the subjobs  i.e. mutates
        certain properties (otherwise all  subjobs would be the same).
        Only  these  properties  may  be mutated  which  are  declared
        'splitable'  in  the   schema.  This  restriction  applies  to
        application  objects to  avoid inconsistencies  if application
        handler is not able to deal with modified arguments.

        In the current implementation the type of the backend cannot
        be changed either.

        """

        raise NotImplementedError

    def validatedSplit(self, job):
        """ Perform splitting using the split() method and validate the mutability
        invariants. If the invariants are broken (or exception occurs in the
        split() method) then SplitterError exception is raised. This method is
        called directly by the framework and should not be modified in the derived
        classes. """

        # try:
        subjobs = self.split(job)
        # except Exception,x:
        #raise SplitterError(x)
        #raise x
        # if not len(subjobs):
        #raise SplitterError('splitter did not create any subjobs')

        cnt = 0
        for s in subjobs:
            if not isType(s.backend, type(stripProxy(job.backend))):
                raise SplitterError('masterjob backend %s is not the same as the subjob (probable subjob id=%d) backend %s' % (job.backend._name, cnt, s.backend._name))
            cnt += 1

        return subjobs

