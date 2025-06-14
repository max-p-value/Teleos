class ProteinTurnover:
    """"""
    def __init__(self, transcription_rate, translation_rate, degradation_rate, mRNA_degradation_rate, dt=1.0):
        self.mRNA = 0.0
        self.protein = 0.0
        self.transcription_rate = transcription_rate
        self.translation_rate = translation_rate
        self.degradation_rate = degradation_rate
        self.mRNA_degradation_rate = mRNA_degradation_rate
        self.dt = dt
        self.time = 0.0
        self.history = []

    def step(self):
        """Advance the simulation by one time step.

        This function updates internal state variables representing
        mRNA and protein levels based on the current rates of 
        transcription, translation, and degradation.

        Effects:
            - Increases mRNA by transcription.
            - Decreases mRNA by degradation.
            - Increases protein by translation of mRNA.
            - Decreases protein by degradation.
            - Appends (time, mRNA, protein) to `self.history`.
        """

        self.mRNA += self.transcription_rate * self.dt
        self.mRNA -= self.mRNA_degradation_rate * self.mRNA * self.dt
        self.protein += self.translation_rate * self.mRNA * self.dt
        self.protein -= self.degradation_rate * self.protein * self.dt
        self.time += self.dt
        self.history.append((self.time, self.mRNA, self.protein))

    def run(self, steps):
        for _ in range(steps):
            self.step()

class RegulatedProteinTurnover:
    """
    Advance the regulated protein turnover simulation by one time step.

    The transcription rate is modulated by an external regulator object
    (e.g., a signaling pathway). If the regulator has an attribute
    `receptor_active` and it is True, the base transcription rate is boosted.

    Parameters:
        dt (float): Timestep duration.
        time (float): Current simulation time.

    Effects:
        - Updates mRNA based on regulated transcription and degradation.
        - Updates protein based on translation and degradation.
        - Adds protein amount to associated compartment.
        - Records time, mRNA, and protein levels to history.
    """
    def __init__(self, base_transcription, transcription_rate, translation_rate, degradation_rate, mRNA_degradation_rate, compartment, dt = 1, regulator=None):
        self.mRNA = 0.0
        self.protein = 0.0
        self.base_transcription = base_transcription
        self.transcription_rate = transcription_rate
        self.translation_rate = translation_rate
        self.degradation_rate = degradation_rate
        self.mRNA_degradation_rate = mRNA_degradation_rate
        self.compartment = compartment
        self.regulator = regulator
        self.dt = dt
        self.time = 0.0
        self.history = []

    def step(self, dt, time):
        transcription_rate = self.base_transcription
        if self.regulator and hasattr(self.regulator, "receptor_active"):
            if self.regulator.receptor_active:
                transcription_rate *= 3  # Boost when activated

        self.mRNA += transcription_rate * dt
        self.mRNA -= self.mRNA_degradation_rate * self.mRNA * dt
        self.protein += self.translation_rate * self.mRNA * dt
        self.protein -= self.degradation_rate * self.protein * dt
        self.compartment.add("proteinX", self.protein * dt)
        self.history.append((self.time, self.mRNA, self.protein))
        self.time += dt