from ..decorators import *
from ..Errors import *
from numbers import Real


@validate_args([int])
@ignite_global
def helper_text_size(self, *args):
    self.font_settings['size'] = args[0]
    self.canvas.font = f"{self.font_settings['size']}px {self.font_settings['font']}"


@validate_args([str])
@ignite_global
def helper_text_align(self, *args):
    if args[0] not in ['left', 'right', 'center']:
        raise ArgumentConditionError("text_align", None, '"left", "right", or "center"', args[0])

    self.canvas.text_align = args[0]


@validate_args([object, Real, Real])
@ignite_global
def helper_text(self, *args):
    # Reassigning the properties gets around a bug with the properties not being used.
    self.canvas.font = self.canvas.font
    self.canvas.text_baseline = self.canvas.text_baseline
    self.canvas.text_align = self.canvas.text_align

    self.canvas.fill_text(str(args[0]), args[1], args[2])
