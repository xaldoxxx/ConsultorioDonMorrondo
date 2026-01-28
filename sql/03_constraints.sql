
ALTER TABLE historia_clinica
ADD CONSTRAINT fk_historia_paciente
FOREIGN KEY (paciente_id) REFERENCES paciente(id),
ADD CONSTRAINT uq_paciente_historia
UNIQUE (paciente_id);
