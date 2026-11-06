"""Reviewed physical status and derivation destinations, not keyword guesses.

Definitions, postulates, empirical models and numerical reference values are
explicit starting points. Everything else is a result and must have a proof.
Number lists refer to the supplied textbook's own equation numbering.
"""
LABELS = {
    'derived': 'Derived result', 'definition': 'Definition',
    'law': 'Fundamental law / postulate', 'model': 'Model / constitutive input',
    'reference': 'Reference value / chosen condition', 'notation': 'Mathematical notation',
}
SOURCE = {}


def G(ch, numbers, slug, kind='derived'):
    for item in numbers.split():
        if ':' in item:
            a, b = map(int, item.split(':'))
            values = range(a, b+1)
        else:
            values = [int(item)]
        for n in values:
            key = f'{ch}-{n}'
            assert key not in SOURCE, key
            SOURCE[key] = dict(kind=kind, topic=slug)


G(1, '8', 'density', 'definition')
G(2, '1 2 3 4 7 8', 'rates-of-change', 'definition')
G(2, '9', 'rates-of-change')
G(2, '11 15:18', 'constant-acceleration')
G(3, '2 3 5 6 10:12', 'vector-components')
G(3, '7', 'vector-components', 'definition')
G(3, '20 24', 'vector-products', 'definition')
G(3, '22 26', 'vector-products')
G(4, '1 2 8 10 15 16', 'rates-of-change', 'definition')
G(4, '3 4 11 17', 'vector-components')
G(4, '21:26', 'projectile-motion')
G(4, '34 35', 'centripetal-acceleration')
G(4, '44 45', 'relative-motion')
G(5, '1', 'newtons-second-law', 'law')
G(5, '2 8 12', 'newtons-second-law')
G(5, '3', 'units-and-dimensions', 'definition')
G(6, '1 2', 'friction', 'model')
G(6, '14', 'terminal-speed', 'model')
G(6, '16', 'terminal-speed')
G(6, '17 18', 'centripetal-acceleration')
G(7, '1 7 8 10 11 12 15 16 32 36', 'work-energy')
G(7, '20 21', 'spring-work', 'model')
G(7, '25 26', 'spring-work')
G(7, '42 43', 'power', 'definition')
G(7, '47 48', 'power')
G(8, '1', 'potential-energy', 'definition')
G(8, '6 7 9 22', 'potential-energy')
G(8, '11', 'spring-work')
G(8, '12', 'mechanical-energy', 'definition')
G(8, '17 18 24 25 26 31 33 36 37', 'mechanical-energy')
G(8, '35', 'first-law', 'law')
G(8, '40 41', 'power', 'definition')
G(9, '5 8 22', 'center-of-mass', 'definition')
G(9, '14 25', 'center-of-mass')
G(9, '23', 'newtons-second-law', 'law')
G(9, '27 31 32 35 42 43 50 51 77 78', 'momentum-and-impulse')
G(9, '30', 'momentum-and-impulse', 'definition')
G(9, '37 40 87 88', 'rocket')
G(9, '67 68', 'elastic-collisions')
G(10, '1 2 4:8', 'rotational-kinematics', 'definition')
G(10, '12:20 22 23', 'rotational-kinematics')
G(10, '33 35', 'rotational-energy', 'definition')
G(10, '34', 'rotational-energy')
G(10, '36', 'parallel-axis')
G(10, '39:41 45', 'angular-momentum')
G(10, '52:55', 'power')
G(11, '2 5 6', 'rolling')
G(11, '10 46', 'gyroscope')
G(11, '14 18 26', 'angular-momentum', 'definition')
G(11, '15:17 19:21 23 29 31 32 33', 'angular-momentum')
G(12, '3 5 7 8 9', 'static-equilibrium')
G(12, '22:25', 'elasticity', 'model')
G(13, '1', 'orbital-speed', 'law')
G(13, '5', 'gravity-sphere-orbits', 'law')
G(13, '6 10 11 19 22 38 40 42', 'gravity-sphere-orbits')
G(13, '21 28', 'escape-speed')
G(13, '34', 'orbital-speed')
G(14, '1 2', 'density', 'definition')
G(14, '3 4', 'hydrostatic-pressure', 'definition')
G(14, '7 8 16 19', 'hydrostatic-pressure')
G(14, '24 25 29', 'bernoulli')
G(15, '1', 'simple-harmonic-motion', 'definition')
G(15, '2:7 12 13', 'simple-harmonic-motion')
G(15, '23 29', 'physical-pendulums')
G(15, '28', 'pendulum')
G(15, '42 43 44 46', 'damped-driven')
G(16, '2 13 17 33 51', 'travelling-wave-energy')
G(16, '5 9', 'travelling-wave-energy', 'definition')
G(16, '26', 'wave-speed')
G(16, '60 66', 'standing-waves')
G(17, '3', 'sound-speed')
G(17, '12 13 14 21:25 27 28 39 41 46 57', 'sound-energy-pipes')
G(17, '26 29', 'sound-energy-pipes', 'definition')
G(17, '47', 'doppler')
G(18, '6 7 8 12', 'thermal-expansion', 'definition')
G(18, '9 10 13 14 16', 'thermal-expansion')
G(18, '25', 'first-law')
G(18, '26 27', 'first-law', 'law')
G(18, '32', 'heat-conduction')
G(18, '38 39', 'planck-radiation')
G(19, '1 7 39 46', 'heat-capacities', 'definition')
G(19, '2 3 4', 'heat-capacities')
G(19, '5 9 21', 'ideal-gas')
G(19, '14', 'isothermal-work')
G(19, '22 25 27 31 35', 'gas-statistics')
G(19, '24', 'equipartition')
G(19, '41 43 44 45 49 51', 'heat-capacities')
G(19, '53', 'adiabatic-gas')
G(20, '1', 'entropy', 'definition')
G(20, '2 3 4', 'entropy')
G(20, '5', 'entropy', 'law')
G(20, '11', 'carnot', 'definition')
G(20, '12 13', 'carnot')
G(20, '14', 'refrigerator', 'definition')
G(20, '15 16', 'refrigerator')
G(20, '20', 'statistical-entropy')
G(20, '21', 'statistical-entropy', 'model')
G(21, '3', 'current-drift', 'definition')
G(21, '4', 'coulomb', 'law')
G(22, '1', 'electric-field', 'definition')
G(22, '3 9 26 28', 'charge-distributions')
G(22, '34 38', 'electric-dipole')
G(23, '4', 'gauss-sphere', 'definition')
G(23, '6', 'gauss-sphere', 'law')
G(23, '11 12 13', 'gauss-cylinder-plane')
G(23, '15 16 20', 'gauss-sphere')
G(24, '2', 'electric-potential', 'definition')
G(24, '3 4 9 11 12 18 19 21 26 27 32 40 41 42', 'electric-potential')
G(24, '30', 'charge-distributions')
G(24, '46', 'electric-energy')
G(25, '1', 'parallel-plate-capacitance', 'definition')
G(25, '9', 'parallel-plate-capacitance')
G(25, '14 17 18', 'capacitor-geometries')
G(25, '19 20 36', 'capacitor-networks')
G(25, '21 22 25', 'capacitor-energy')
G(26, '1', 'current-drift', 'definition')
G(26, '4', 'current-flux')
G(26, '7', 'current-drift')
G(26, '8 10 12', 'resistance', 'definition')
G(26, '11 17', 'resistance', 'model')
G(26, '16 26 27 28', 'resistance')
G(26, '22', 'drude')
G(27, '1', 'kirchhoff', 'definition')
G(27, '4 14 16 17 39 40', 'battery-discharge')
G(27, '7 24', 'kirchhoff')
G(27, '33 34', 'rc-circuit')
G(28, '2', 'magnetic-orbit', 'law')
G(28, '15:19', 'magnetic-orbit')
G(28, '26 28 37 38 39', 'magnetic-wire')
G(29, '3 14', 'ampere-wire', 'law')
G(29, '4', 'ampere-wire')
G(29, '9 13 24 27', 'magnetic-geometries')
G(29, '23', 'solenoid')
G(30, '1 19 28', 'inductor-energy', 'definition')
G(30, '2 5', 'faraday')
G(30, '4 20', 'faraday', 'law')
G(30, '35 49', 'inductor-energy')
G(30, '31 41 45 55 64 65', 'rl-mutual')
G(31, '1 2 4 11 12 13', 'lc-oscillations')
G(31, '24 25 26 65 71 76 79 80 82', 'ac-power-transformers')
G(31, '28', 'ac-impedance', 'model')
G(31, '29 60 61 63', 'ac-impedance')
G(32, '1 3 4 5', 'displacement-current', 'law')
G(32, '10', 'displacement-current', 'definition')
G(32, '11', 'displacement-current')
G(32, '22', 'magnetic-moments', 'model')
G(32, '23 29', 'quantum-angular')
G(32, '25', 'magnetic-moments', 'definition')
G(32, '24 26 27 28 30 31 32', 'magnetic-moments')
G(32, '38', 'curie-law', 'definition')
G(32, '39', 'curie-law')
G(33, '1 2 3 5', 'em-wave-equation')
G(33, '19 26', 'em-intensity')
G(33, '27', 'sound-energy-pipes')
G(33, '32:35', 'radiation-pressure')
G(33, '36 38 40 45 49', 'polarization-refraction')
G(34, '3 4', 'spherical-mirror')
G(34, '5', 'thin-lens', 'definition')
G(34, '6 9', 'thin-lens')
G(34, '8 10 12 14 15', 'refracting-instruments')
G(35, '6', 'polarization-refraction')
G(35, '14 16 22 23', 'double-slit')
G(35, '36 37', 'thin-film')
G(36, '3 5 6', 'single-slit')
G(36, '12 14 19 34', 'apertures-bragg')
G(36, '25 28 29 30 31 32', 'diffraction-grating')
G(37, '7 8 9', 'time-dilation')
G(37, '13 21 29', 'lorentz-transform')
G(37, '32 36 37', 'light-doppler')
G(37, '42 47 48', 'relativistic-energy', 'definition')
G(37, '52 54 55', 'relativistic-energy')
G(37, '50', 'binding-energy')
G(38, '2', 'photons', 'law')
G(38, '5 7', 'photons')
G(38, '11', 'compton')
G(38, '14 15', 'planck-radiation')
G(38, '19 28', 'quantum-foundations')
G(38, '38 39', 'tunneling')
G(39, '4', 'particle-in-box')
G(39, '5 6 37 38', 'atomic-transitions')
G(39, '10 14 19 20 45', 'quantum-normalization')
G(39, '23', 'hydrogen', 'model')
G(39, '34', 'hydrogen-quantum')
G(40, '1', 'atomic-transitions')
G(40, '2 3 6 7 9 10 12 13', 'quantum-angular')
G(40, '8', 'magnetic-moments', 'definition')
G(40, '17 22', 'magnetic-moments')
G(41, '2 4 5 7 9 11', 'electron-gas-states')
G(41, '3', 'electron-gas-states', 'definition')
G(41, '6', 'fermi-dirac')
G(42, '3', 'nuclear-size-fusion')
G(42, '6 8', 'binding-energy', 'definition')
G(42, '7', 'binding-energy')
G(42, '15 16 17', 'radioactive-decay')
G(43, '16', 'nuclear-size-fusion')
G(44, '19', 'cosmological-redshift')
G(44, '21', 'cosmological-redshift', 'reference')

# Explicit non-derived note blocks; all remaining blocks require a proof section.
# Main blocks that combine an input with a consequence remain classified derived.
NOTE_INPUTS = {
    'units-and-dimensions': {'main':'definition','step-1':'definition'},
    'density': {'main':'definition','step-1':'definition','step-2':'definition'},
    'rates-of-change': {'main':'definition','step-1':'definition','step-2':'definition','step-3':'definition'},
    'vector-components': {'step-1':'definition','step-2':'definition'},
    'vector-products': {'main':'definition','step-3':'definition'},
    'newtons-second-law': {'step-2':'law'},
    'friction': {'main':'model'},
    'terminal-speed': {'step-1':'model'},
    'spring-work': {'step-1':'model'},
    'potential-energy': {'step-2':'definition'},
    'center-of-mass': {'step-1':'definition'},
    'rotational-energy': {'step-3':'definition'},
    'angular-momentum': {'step-1':'definition'},
    'elasticity': {'step-1':'definition','step-2':'definition','step-3':'model'},
    'orbital-speed': {'step-1':'law'},
    'sound-speed': {'step-1':'model'},
    'first-law': {'step-1':'law'},
    'coulomb': {'main':'law','step-1':'law'},
    'charge-conservation': {'main':'law'},
    'gauss-sphere': {'step-1':'law'},
    'resistance': {'step-1':'model','step-3':'definition'},
    'current-drift': {'step-1':'definition'},
    'magnetic-orbit': {'step-1':'law'},
    'ampere-wire': {'step-1':'law'},
    'faraday': {'step-1':'definition','step-2':'law'},
    'inductor-energy': {'step-1':'definition'},
    'em-wave-equation': {'step-1':'law'},
    'relativistic-energy': {'step-1':'definition'},
    'photons': {'step-1':'law'},
    'hydrogen': {'step-2':'model'},
    'fermi-dirac': {'step-1':'law'},
    'quark-charges': {'step-1':'model'},
    'cosmological-redshift': {'step-1':'definition','step-2':'model'},
    'rotational-kinematics': {'step-1':'definition'},
    'heat-conduction': {'step-1':'model'},
    'heat-capacities': {'step-2':'definition'},
    'refrigerator': {'step-1':'definition'},
    'statistical-entropy': {'main':'derived','step-4':'model'},
    'quantum-foundations': {'step-1':'law'},
    'quantum-normalization': {'step-1':'law'},
    'quantum-angular': {'step-1':'law'},
    'magnetic-moments': {'step-2':'model'},
    'curie-law': {'step-1':'definition'},
    'drude': {'step-1':'model'},
    'integrals': {'step-1':'definition','step-2':'definition'},
    'boltzmann-weights': {'step-1':'law'},
}
