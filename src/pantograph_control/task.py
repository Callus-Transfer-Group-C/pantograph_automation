# This is the file where everything comes together.
# Because we are using a (relatively) open control loop, sequencing 
# is going to be critical (and complex), and needs to be abstracted away
# from the pantograph ui.

# TaskStack:
# This class (and subclasses) will extend the pyside2 QObject class so that the
# main application can allocate it to a thread appropriately and keep the ui
# responsive. Although it is running at on a seperate thread, the sequence of tasks
# needs to be able to exit (emergency stop) at any time.

# Task:
# This class (and subclasses) will link together the neccessary time-dependant
# trajectories and hardware actions to transfer physical objects. The following
# subclasses will need to be implemented:
#  - LoadNewInDish
#  - EmptyOldInDish
#  - LoadNewOutDish
#  - EmptyOldOutDish
#  - TransferStage1
#  - TransferStage2
# Exact implementation may vary, but the end goal is that the user selects 'run Stage 1'
# with optional parameters (i.e. whether or not to expect a full stack, take pictures, etc.)
# and the TaskStack takes care of the rest.


from pantograph_control import camera, drivers, kinematics, trajectory
from PySide6.QtCore import QObject, Signal, Slot
import time, traceback, sys


# TODO: Implement task
class TaskStack(QObject):
    finished = Signal()  # No arguments
    error = Signal(tuple) # Emits (type, value, traceback)
    progress = Signal(int) # Emits current percentage (0-100)
    message = Signal(str)  # Emits status text updates
    """
    Template for creating tasks used by the ui package.

    Attributes:
        Task attributes

    Methods:
        Task methods
    """

    def __init__(self):
        """
        Initializes the task stack.

        Parameters:
            params

        Returns:
            result

        Raises:
            errors
        """
        self.task_stack = [
            None,
            None,
            None
        ]

        raise NotImplementedError("'TaskStack' has not yet been implemented")
    
    @Slot()
    def run_tasks(self):
        """
        Runs all tasks (in a thread implemented in pantograph_ui)

        Parameters:
            params

        Returns:
            result

        Raises:
            errors
        """
        try:
            self.message.emit("Example message...")
            self.progress.emit(50)

            raise NotImplementedError("'run_tasks' has not yet been implemented")
        
        except Exception:
            self.error.emit(sys.exc_info())

        finally:
            self.finished.emit()

        pass

# TODO: Implement task
class Task:
    """
    Template for creating tasks used by the ui package.

    Attributes:
        Task attributes

    Methods:
        Task methods
    """

    def __init__(self):
        """
        Initializes the task.

        Parameters:
            params

        Returns:
            result

        Raises:
            errors
        """
        raise NotImplementedError("'Task' has not yet been implemented")
    
    def run(self):
        """
        Runs the task (blocking method)

        Parameters:
            params

        Returns:
            result

        Raises:
            errors
        """

        raise NotImplementedError("'run' has not yet been implemented")