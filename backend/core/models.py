from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="drivers")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Piloto"
        verbose_name_plural = "Pilotos"

    def __str__(self):
        return f"{self.number} - {self.name}"


class Event(models.Model):
    name = models.CharField(max_length=150)
    round_number = models.PositiveIntegerField(unique=True)
    circuit = models.CharField(max_length=150, blank=True)
    date = models.DateField(blank=True, null=True)
    has_sprint = models.BooleanField(default=False)
    practice_sessions_count = models.PositiveIntegerField(default=3)
    qualifying_sessions_count = models.PositiveIntegerField(default=3)

    class Meta:
        verbose_name = "Etapa"
        verbose_name_plural = "Etapas"
        ordering = ["round_number"]

    def __str__(self):
        return f"Round {self.round_number} - {self.name}"


class Session(models.Model):
    SESSION_TYPES = [
        ("FP1", "Treino Livre 1"),
        ("FP2", "Treino Livre 2"),
        ("FP3", "Treino Livre 3"),
        ("Q1", "Qualificacao Q1"),
        ("Q2", "Qualificacao Q2"),
        ("Q3", "Qualificacao Q3"),
        ("SPRINT_QUALIFYING", "Qualificacao Sprint"),
        ("SPRINT", "Corrida Sprint"),
        ("RACE", "Corrida"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sessions")
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    session_number = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=100, blank=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["event__round_number", "session_number", "session_type"]
        unique_together = ("event", "session_type", "session_number")

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = dict(self.SESSION_TYPES).get(self.session_type, self.session_type)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event} - {self.name}"


class Result(models.Model):
    STATUS_CHOICES = [
        ("CLASSIFIED", "Classificado"),
        ("DNF", "DNF"),
        ("DNS", "DNS"),
        ("DSQ", "Desclassificado"),
        ("RETIRED", "Retirado"),
        ("NOT_STARTED", "Nao iniciou"),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="results")
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name="results")
    position = models.PositiveIntegerField(blank=True, null=True)
    time = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CLASSIFIED")
    points = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "time", "driver__number"]
        unique_together = ("session", "driver")

    @staticmethod
    def points_for_position(session_type, position):
        if position is None:
            return 0
        if session_type == "SPRINT":
            sprint_points = [8, 7, 6, 5, 4, 3, 2, 1]
            return sprint_points[position - 1] if 1 <= position <= len(sprint_points) else 0
        if session_type == "RACE":
            race_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
            return race_points[position - 1] if 1 <= position <= len(race_points) else 0
        return 0

    def save(self, *args, **kwargs):
        if self.status == "CLASSIFIED" and self.position:
            self.points = self.points_for_position(self.session.session_type, self.position)
        else:
            self.points = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.session} - {self.driver}"
