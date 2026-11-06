"""Additional worked arguments needed by the equation-by-equation review audit."""


def add_supplements(T, S):
    def P(ch, slug, title, formula, symbols, conditions, steps, example, caution):
        T(ch, slug, title, formula, steps[0][1], symbols, conditions,
          [S(*s) for s in steps], example, caution)

    P(4, 'relative-motion', 'Derive Galilean relative velocity and acceleration',
      '𝐯PA = 𝐯PB + 𝐯BA;  𝐚PA = 𝐚PB  (constant 𝐯BA)',
      '𝐫PA: position of particle P from origin A; 𝐫BA: origin B measured from A; t: shared Newtonian time.',
      'Nonrelativistic mechanics, aligned nonrotating axes, and constant relative frame velocity for the acceleration equality.', [
        ('Join the position vectors', 'The displacement from A to P equals the displacement from A to B followed by B to P.', '𝐫PA = 𝐫BA + 𝐫PB'),
        ('Differentiate using a shared time', 'In Galilean mechanics both frames use the same time coordinate. Differentiate each position vector.', '𝐯PA = d𝐫BA/dt + d𝐫PB/dt = 𝐯BA + 𝐯PB'),
        ('Differentiate again', 'If B translates at constant velocity, its second derivative relative to A is zero.', '𝐚PA = 𝐚BA + 𝐚PB = 𝐚PB'),
        ('Identify the limit of the model', 'Rotating frames introduce additional acceleration terms; relativistic frames do not share a universal time coordinate.', '', ('How are velocities combined relativistically?', 'lorentz-transform')),
      ], 'A train moving east at 20 m/s and a passenger walking east at 2 m/s give a passenger ground velocity of 22 m/s.',
      'The acceleration equality requires nonrotating frames in uniform relative translation.')

    P(7, 'power', 'Derive translational and rotational power', 'P = 𝐅 · 𝐯;  dW = τ dθ;  Paxis = τω',
      'P: instantaneous power; 𝐅: force; 𝐯: application-point velocity; τ: signed axial torque; θ: angle in radians.',
      'Particle work, or a rigid body rotating about a fixed axis; sum individual contributions for multiple forces.', [
        ('Start from mechanical work', 'Work is the accumulated component of force along displacement. Its instantaneous rate defines power.', 'dW = 𝐅 · d𝐫;  P ≡ dW/dt'),
        ('Divide by the elapsed time', 'Since d𝐫/dt is velocity, the work rate is the dot product with velocity.', 'P = 𝐅 · (d𝐫/dt) = 𝐅 · 𝐯'),
        ('Use the circular displacement', 'At radius r the tangential displacement is r dθ. Only tangential force contributes; its moment is τ = rFt.', 'dW = Ft r dθ = τ dθ'),
        ('Accumulate or differentiate', 'Integrate torque for finite work; for constant torque it leaves the integral. Divide differential work by dt for power.', 'W = ∫ τ dθ;  Wconstant τ = τΔθ;  P = τ dθ/dt = τω'),
      ], 'A constant 5 N·m torque through 3 rad does 15 J of work. At 2 rad/s its power is 10 W.',
      'Use the velocity of the point where the force acts, not automatically the centre-of-mass velocity.')

    P(9, 'elastic-collisions', 'Derive one-dimensional elastic collision velocities',
      'v₁ = [(m₁ − m₂)u₁ + 2m₂u₂]/(m₁ + m₂);  v₂ = [2m₁u₁ + (m₂ − m₁)u₂]/(m₁ + m₂)',
      'u₁,u₂: initial velocities; v₁,v₂: final velocities; m₁,m₂: positive masses, with all velocities signed on one axis.',
      'Isolated two-body collision, conserved kinetic energy, and a nontrivial collision rather than unchanged velocities.', [
        ('Conserve the two quantities', 'An isolated elastic collision conserves total momentum and total kinetic energy.', 'm₁u₁ + m₂u₂ = m₁v₁ + m₂v₂;  m₁u₁² + m₂u₂² = m₁v₁² + m₂v₂²'),
        ('Factor differences of squares', 'Rearrange each conservation equation so the change of body 1 balances the change of body 2. Divide the energy equation by the momentum equation when the exchange is nonzero.', 'u₁ + v₁ = u₂ + v₂'),
        ('Reverse relative velocity', 'The previous equation means approach and separation have equal speed in the relative coordinate.', 'v₂ − v₁ = u₁ − u₂'),
        ('Solve the two linear equations', 'Substitute v₂ = v₁ + u₁ − u₂ in momentum conservation and isolate v₁; then recover v₂. Setting u₂ = 0 gives the textbook stationary-target formulas.', 'u₂ = 0 ⇒ v₁ = (m₁ − m₂)u₁/(m₁ + m₂),  v₂ = 2m₁u₁/(m₁ + m₂)'),
      ], 'Equal masses with the second initially at rest exchange velocities: v₁ = 0 and v₂ = u₁.',
      'For an inelastic collision, momentum conservation alone does not determine both final velocities; another condition is needed.')

    P(9, 'rocket', 'Derive the ideal rocket equation and momentum flux', 'M dv = −vrel dM;  Δv = vrel ln(Mi/Mf)',
      'M: remaining rocket plus fuel mass; dM < 0: mass loss; vrel > 0: backward exhaust speed relative to rocket; R = −dM/dt.',
      'One-dimensional ideal exhaust, negligible external impulse, constant relative exhaust speed for the integrated logarithm.', [
        ('Use a closed system during ejection', 'Include rocket and the small exhaust parcel together, so their total momentum is conserved during the short ejection interval.', 'Mv = (M + dM)(v + dv) + (−dM)(v − vrel)'),
        ('Keep first-order changes', 'Expand and discard the product dM dv. The original Mv cancels, leaving a gain in rocket momentum opposite the expelled relative momentum.', 'M dv = −vrel dM'),
        ('Divide by time', 'Replacing the negative mass-loss rate by positive R gives thrust and instantaneous acceleration.', 'Ma = Rvrel'),
        ('Integrate the changing mass', 'Mass cannot be treated as constant during a finite burn. Divide by M and integrate between initial and final masses.', 'vf − vi = −vrel ∫[Mi,Mf] dM/M = vrel ln(Mi/Mf)'),
        ('Relate to a stream hitting a target', 'The same momentum-flux reasoning gives force on a target opposite the rate of the stream’s momentum change.', 'Ftarget = −(Δm/Δt)Δvstream'),
      ], 'With exhaust speed 2000 m/s and Mi/Mf = 2, ideal Δv is about 1386 m/s.',
      'Adding external gravity or drag changes the velocity gain. Use a clear control-volume boundary for open systems.')

    P(10, 'rotational-kinematics', 'Derive the rotational kinematic equations',
      'ω = ω₀ + αt;  θ − θ₀ = ω₀t + ½αt²;  ω² − ω₀² = 2α(θ − θ₀)',
      'θ: signed angular coordinate in radians; ω = dθ/dt; α = dω/dt; r: fixed perpendicular radius.',
      'Fixed-axis rotation; α constant for the three finite-interval equations.', [
        ('Define angular rates and radian distance', 'An angular coordinate is arc distance divided by radius. Its time derivatives define angular velocity and acceleration.', 'θ ≡ s/r;  ω ≡ dθ/dt;  α ≡ dω/dt'),
        ('Integrate constant angular acceleration', 'Accumulating α gives ω, then accumulating ω gives θ. This is the same mathematical operation used for straight-line motion.', 'ω = ω₀ + αt;  Δθ = ω₀t + ½αt²', ('Why does accumulation introduce ½?', 'integrals')),
        ('Eliminate time', 'For a straight-line angular-velocity graph its average is (ω₀ + ω)/2. Substitute αt = ω − ω₀ to eliminate t.', 'Δθ = ½(ω₀ + ω)t = ωt − ½αt²;  2αΔθ = ω² − ω₀²'),
        ('Differentiate the arc relation', 'For fixed r, s = rθ implies tangential speed rω and tangential acceleration rα. Circular curvature supplies the separate radial component.', 'v = rω;  at = rα;  ar = v²/r = rω²;  T = 2π/ω'),
      ], 'At α = 2 rad/s², starting at rest for 3 s gives ω = 6 rad/s and angular displacement 9 rad.',
      'An angular acceleration can coexist with radial acceleration. They are perpendicular components, not interchangeable quantities.')

    P(11, 'gyroscope', 'Derive rolling acceleration and slow gyroscopic precession',
      'adown = g sin θ/[1 + I/(MR²)];  Ω = Mgr/(Iω)',
      'I: axial inertia; R: rolling radius; θ: incline angle; r: gyroscope centre-of-mass lever arm; Ω: precession rate.',
      'For rolling: no slip on a fixed slope. For precession: fast spin with nearly steady horizontal angular momentum, negligible nutation.', [
        ('Combine translation and rotation for rolling', 'Friction up the slope supplies the rolling torque, while gravity drives translation. Apply no slip to relate a and α.', 'Ma = Mg sin θ − f;  fR = Iα;  a = Rα'),
        ('Eliminate friction', 'Use f = Ia/R² and collect the terms proportional to a. An axis up the ramp reverses the resulting acceleration sign.', 'a(M + I/R²) = Mg sin θ'),
        ('Describe the changing direction of spin momentum', 'For a nearly horizontal spin angular momentum L = Iω, turning its direction by dφ changes its vector by magnitude L dφ.', '|d𝐋/dt| = LΩ'),
        ('Supply the gravitational torque', 'The weight torque has magnitude Mgr in this geometry. Equate it to the angular-momentum turning rate.', 'Mgr = IωΩ ⇒ Ω = Mgr/(Iω)', ('Why does torque equal angular-momentum rate?', 'angular-momentum')),
      ], 'Doubling the spin rate halves this ideal slow-precession rate, provided the fast-spin approximation still holds.',
      'The displayed precession formula is an approximation, not the full solution for an arbitrary initial gyroscope motion.')

    P(13, 'gravity-sphere-orbits', 'Derive spherical gravity and orbital energy',
      'goutside = GM/r²;  Finside = GMmr/R³;  Eellipse = −GMm/(2a)',
      'M,R: spherical body mass and radius; a: orbital semimajor axis; r: centre-to-particle distance; h: specific angular momentum.',
      'Newtonian inverse-square gravity and superposition; uniform density for the interior linear field; an isolated bound two-body orbit with m ≪ M.', [
        ('Evaluate the spherical shell integral', 'For a shell of radius R and total mass M, symmetry gives U = −GMm/2 times the integral from −1 to 1 of du/√(r² + R² − 2rRu). The integral is [(r + R) − |r − R|]/(rR), hence U = −GMm/max(r,R). Differentiating gives zero interior force and the exterior inverse-square field.', 'Uoutside = −GMm/r;  Uinside shell = −GMm/R'),
        ('Count only the enclosed mass inside a solid sphere', 'Shells outside r give zero force; uniform density gives Menc = M(r/R)³. Newton’s law then gives the local acceleration and force.', 'Finside = GmMenc/r² = GMmr/R³;  goutside = F/m = GM/r²'),
        ('Evaluate circular-orbit energy', 'Circular force balance gives mv² = GMm/r. Thus K = GMm/(2r), and adding U = −GMm/r gives the total.', 'Ecircular = −GMm/(2r)'),
        ('Use the two turning points of an ellipse', 'At pericentre rp and apocentre ra radial speed vanishes. Equate E/m = h²/(2rp²) − GM/rp to the corresponding expression at ra. Eliminating h yields E/m = −GM/(rp + ra).', 'rp + ra = 2a ⇒ E = −GMm/(2a)'),
        ('Add pair energies once', 'For multiple point masses, assemble each pair once, just as for electric energy, with every pair gravitationally attractive.', 'U = −Σ[i<j] Gmimj/rij'),
      ], 'A uniform sphere’s inward acceleration is zero at its centre and rises linearly to GM/R² at its surface.',
      'The exterior point-mass result needs spherical symmetry; the linear interior result additionally needs uniform density.')

    P(15, 'physical-pendulums', 'Derive torsion and physical-pendulum periods', 'Ttorsion = 2π√(I/κ);  Tphysical ≈ 2π√(I/(Mgh))',
      'I: inertia about the pivot; κ: torsion constant; h: pivot-to-centre-of-mass distance; θ: angular displacement.',
      'Rigid body, frictionless fixed pivot, linear torsional restoring torque or small gravitational angle.', [
        ('Apply rotational dynamics', 'Fixed-axis angular acceleration is torque divided by inertia.', 'Iθ̈ = τ'),
        ('Use the torsion model', 'A linear torsion wire supplies τ = −κθ. Compare θ̈ = −(κ/I)θ with harmonic motion.', 'ωtorsion² = κ/I ⇒ Ttorsion = 2π√(I/κ)'),
        ('Find the gravitational torque', 'Weight acts at the centre of mass in uniform gravity. Its restoring torque is −Mgh sin θ, approximately −Mghθ for small angles.', 'Iθ̈ ≈ −Mghθ'),
        ('Identify the physical-pendulum frequency', 'The coefficient of minus displacement is again ω². For a point mass I = Mℓ² and h = ℓ, recovering the simple-pendulum period.', 'ωphysical² = Mgh/I ⇒ Tphysical = 2π√(I/(Mgh))'),
      ], 'A uniform rod pivoted at one end has I = ML²/3 and h = L/2, giving T ≈ 2π√(2L/(3g)).',
      'Use inertia about the actual pivot. A central inertia alone gives the wrong physical-pendulum period.')

    P(15, 'damped-driven', 'Derive damped oscillations and resonance',
      'x = A exp(−bt/(2m))cos(ω′t + φ);  ω′² = k/m − b²/(4m²)',
      'b: linear damping coefficient; F₀,ωd: sinusoidal drive amplitude and frequency; A: displacement envelope scale.',
      'Linear restoring force −kx and linear drag −bẋ. The oscillatory free solution needs b² < 4mk.', [
        ('Write the force equation', 'Add spring, damping and optional sinusoidal driving forces.', 'mẍ + bẋ + kx = F₀ cos(ωdt)'),
        ('Solve the undriven characteristic equation', 'For x ∝ exp(st), the equation becomes ms² + bs + k = 0. Its underdamped roots are a negative real part plus conjugate imaginary parts.', 's = −b/(2m) ± i√(k/m − b²/(4m²))'),
        ('Convert complex exponentials to real motion', 'The real solution is a sinusoid multiplied by the decaying envelope. Weak-damping cycle-averaged energy scales as the square of that envelope.', '⟨E⟩ ≈ ½kA² exp(−bt/m)'),
        ('Solve for the driven amplitude', 'Insert a sinusoidal steady response and combine in-phase and quadrature force terms. The velocity amplitude is ωd times the displacement amplitude.', 'X = F₀/√[(k − mωd²)² + b²ωd²]'),
        ('Locate resonance precisely', 'Dividing the squared velocity-amplitude denominator by ωd² shows it is minimized when k/ωd − mωd = 0. Displacement resonance is slightly lower when it exists.', 'ωvelocity,max = √(k/m);  ωdisplacement,max² = k/m − b²/(2m²)'),
      ], 'If b/(2m) = 1 s⁻¹, the free amplitude envelope decreases by a factor e in one second.',
      'Amplitude-squared energy decay is a cycle-average weak-damping statement, not an exact instantaneous sinusoid-free expression.')

    P(16, 'travelling-wave-energy', 'Derive travelling-wave phase, speed and energy flow',
      'v = ω/k = fλ;  Pavg,string = ½μvω²A²',
      'A: transverse amplitude; μ: string linear density; k = 2π/λ; ω = 2πf; 𝒯: string tension.',
      'Small-amplitude sinusoidal wave on a uniform ideal string. Interference formulas assume linear superposition.', [
        ('Track a fixed phase', 'A point of unchanged phase satisfies kx − ωt = constant. Differentiating gives its propagation speed; phase repeats every 2π.', 'v = dx/dt = ω/k;  kλ = 2π;  ωT = 2π'),
        ('Differentiate displacement', 'For y = A sin(kx − ωt), local transverse velocity is −Aω cos(kx − ωt) and local slope is Ak cos(kx − ωt).', '∂y/∂t = −Aω cos(phase);  ∂y/∂x = Ak cos(phase)'),
        ('Compute string power crossing a section', 'Tension transfers energy at rate −𝒯(∂y/∂x)(∂y/∂t). Use 𝒯 = μv², k = ω/v and average cos² = ½.', 'Pavg = ½𝒯Ak Aω = ½μvω²A²'),
        ('Superpose two waves algebraically', 'The trigonometric identity sin u + sin v = 2sin[(u+v)/2]cos[(u−v)/2] yields both phase interference and counterpropagating standing patterns.', 'ysame direction = 2A cos(φ/2)sin(kx − ωt + φ/2);  ystanding = 2A sin(kx)cos(ωt)'),
      ], 'Doubling sinusoidal amplitude multiplies average transported power by four at unchanged frequency and medium.',
      'Propagation velocity differs from the local transverse velocity of a string element.')

    P(17, 'sound-energy-pipes', 'Derive sound intensity, pipe modes, beats and Mach angle',
      'I = ½ρvω²sm²;  fopen = nv/(2L);  fone closed = nv/(4L), n odd',
      'sm: displacement amplitude; B: bulk modulus; ρ: density; v: sound speed; L: pipe length; vs: supersonic source speed.',
      'Linear plane sound, ideal pipe boundaries without end correction, coherent waves for beats, and uniform sound speed for Mach geometry.', [
        ('Differentiate compression', 'For displacement s = sm cos(kx − ωt), pressure change is −B∂s/∂x. With B = ρv² and k = ω/v this sets the pressure amplitude.', 'Δp = Bksm sin(phase);  Δpm = ρvωsm'),
        ('Average pressure times particle velocity', 'Local particle velocity is ∂s/∂t = ωsm sin(phase). The power per area is their product, whose sine squared averages to ½.', 'I = ⟨Δp ∂s/∂t⟩ = ½ρvω²sm²'),
        ('Spread conserved power over a sphere', 'An isotropic lossless source delivers the same total power through every surrounding sphere. Divide that power by area 4πr².', 'I(r) = Ps/(4πr²)'),
        ('Enforce pipe boundary conditions', 'Open ends are approximate pressure nodes (displacement antinodes), while a closed end is a displacement node. Two open ends fit n half wavelengths; unlike ends fit odd quarter wavelengths.', 'λopen = 2L/n;  λone closed = 4L/n, n = 1,3,5,…'),
        ('Translate path difference into phase', 'Every wavelength advances phase by 2π. Two initially in-phase equal waves reinforce for integer-wavelength path differences and cancel for half-integer differences.', 'δ = 2πΔL/λ;  constructive: ΔL = mλ;  destructive: ΔL = (m + ½)λ'),
        ('Add close frequencies', 'The cosine sum identity gives a rapidly oscillating carrier times a slow envelope. Consecutive envelope magnitudes repeat at the absolute frequency difference.', 'fbeat = |f₁ − f₂|'),
        ('Construct the Mach cone', 'After time t the source advances vst while an earlier wavefront has radius vt. Their tangent cone has half-angle satisfying opposite over hypotenuse.', 'sin θ = vt/(vst) = v/vs'),
      ], 'Two tones at 440 and 444 Hz beat four times per second. For a source at Mach 2, the cone half-angle is 30°.',
      'The decibel expression β ≡ 10log₁₀(I/I₀) is a definition of a level, not another propagation law.')

    P(18, 'thermal-expansion', 'Derive finite expansion and heat-capacity formulas',
      'ΔL ≈ αLΔT;  β ≈ 3α;  Q = ∫ C(T)dT',
      'α: fractional linear expansion per kelvin; β: fractional volume expansion per kelvin; C: heat capacity for a specified process; c = C/m.',
      'Small temperature change, isotropic solid for β = 3α, fixed mass, and heat capacity measured along the specified process without a phase transition.', [
        ('State the differential coefficients', 'Linear expansivity is defined by fractional length change per temperature change. Approximating α and the reference length as constant gives the familiar finite-change formula.', 'α ≡ (1/L)dL/dT ⇒ ΔL ≈ αLΔT'),
        ('Expand all three dimensions', 'For an isotropic solid, each side gains a factor 1 + αΔT. Multiply the factors and neglect second and higher powers.', 'Vf = Vi(1 + αΔT)³ ≈ Vi(1 + 3αΔT)'),
        ('Integrate the specified heat capacity', 'Define C along the chosen process by δQ = C(T)dT. Constant C gives Q = CΔT; specific heat c = C/m gives Q = mcΔT.', 'Q = ∫[Ti,Tf] C(T)dT ⇒ Qconstant C = CΔT = mcΔT'),
        ('Separate a change of phase', 'Latent heat per mass is defined by L = Q/m for the specified transition conditions. At coexistence the heat goes into changing phase rather than raising temperature.', 'Qtransition = mL'),
      ], 'For α = 10⁻⁵ K⁻¹ and ΔT = 20 K, a 1 m isotropic rod lengthens by about 0.20 mm.',
      'Expansion coefficients and heat capacities vary with temperature. Heating and pressure constraints must be stated before choosing C.')

    P(18, 'heat-conduction', 'Derive heat conduction through a slab', 'P = kA(TH − TC)/L',
      'k: thermal conductivity; A: slab cross-sectional area; L: thickness; TH > TC: face temperatures.',
      'Steady one-dimensional conduction, uniform conductivity, no internal heating, and negligible side losses.', [
        ('State the local constitutive law', 'Fourier’s empirical law relates heat flux to a temperature gradient. It is a material-response input.', 'jx = −k dT/dx'),
        ('Use steady energy conservation', 'With no internal sources, the same power crosses every section. For constant A and k the gradient is therefore constant.', 'P = Ajx = −kA dT/dx = constant'),
        ('Integrate across the slab', 'Let x increase from the hot face to the cold face. Integrate dT/dx = −P/(kA) over thickness L.', 'TC − TH = −PL/(kA)'),
        ('Solve and interpret the sign', 'Positive P points from hot to cold. Thermal resistance L/(kA) plays the role of resistance to energy flow.', 'P = (TH − TC)/[L/(kA)]'),
      ], 'Doubling slab thickness halves the steady conducted power if the same face temperatures are maintained.',
      'Radiative T⁴ laws follow from thermal photon statistics and have a separate derivation.',)

    P(19, 'gas-statistics', 'Derive Maxwell speeds and mean free path',
      'vrms = √(3kBT/m);  vavg = √(8kBT/(πm));  vp = √(2kBT/m);  λ = 1/(√2πd²nN)',
      'm: molecular mass; nN = N/V: number density; d: hard-sphere collision diameter; a = m/(2kBT).',
      'Classical dilute equilibrium ideal gas; hard-sphere collision model for the mean free path.', [
        ('Normalize momentum probabilities', 'Independent Cartesian velocities have Boltzmann weights exp(−avx²). The Gaussian normalization in three dimensions is (a/π)³ᐟ².', 'f(𝐯) = (a/π)³ᐟ² exp(−av²)', ('Why is molecular kinetic energy tied to temperature?', 'equipartition')),
        ('Count velocity-space shells', 'Velocities of speed v occupy a spherical shell of volume 4πv²dv. Multiply the Cartesian probability density by that shell factor.', 'P(v) = 4π(a/π)³ᐟ²v² exp(−av²)'),
        ('Compute moments and the maximum', 'Integrating vP(v) gives the mean; equipartition gives ⟨v²⟩. Set d[ln P]/dv = 2/v − 2av = 0 to get the most probable speed.', 'vavg = 2/(√π√a);  vrms = √(3/(2a));  vp = 1/√a'),
        ('Count collision opportunities', 'A stationary-target model sweeps collision volume πd²v dt and predicts rate nNπd²v. Thermal motion of identical targets increases mean relative speed to √2 times mean molecular speed.', 'collision rate = √2 nNπd²vavg'),
        ('Divide distance rate by collision rate', 'Mean free path is mean distance per collision. The molecular speed cancels between path length per second and collisions per second.', 'λ = vavg/(√2 nNπd²vavg) = 1/(√2 nNπd²)'),
      ], 'The three characteristic speeds satisfy vp < vavg < vrms. A narrower collision diameter gives a longer mean free path at fixed density.',
      'Mean free path is a statistical average. The √2 correction is tied to the thermal hard-sphere model, not a universal collision constant.')

    P(19, 'heat-capacities', 'Derive ideal-gas internal energy and heat capacities',
      'U = (f/2)nRT;  CV = fR/2;  CP = CV + R',
      'f: number of active independent quadratic degrees of freedom; CV,CP: molar heat capacities; n: fixed mole count.',
      'Classical ideal gas, active modes constant over the range; pressure–volume work only.', [
        ('Add equipartition terms', 'Each active quadratic term contributes kBT/2 per molecule. Multiply by f and the molecule count N = nNA.', 'U = Nf kBT/2 = nfRT/2', ('Derive the energy per quadratic term', 'equipartition')),
        ('Differentiate at constant volume', 'With no volume work, Q = ΔU. The molar constant-volume heat capacity is the temperature derivative divided by n.', 'CV ≡ (1/n)(∂U/∂T)V = fR/2'),
        ('Include work at constant pressure', 'The ideal-gas equation gives pΔV = nRΔT. At fixed pressure the heat must supply both the internal-energy increase and this work.', 'nCPΔT = nCVΔT + nRΔT ⇒ CP = CV + R'),
        ('Integrate over a finite temperature change', 'Ideal-gas internal energy depends on temperature. Constant CV gives ΔU = nCVΔT for any path; a chosen energy reference yields U = nCVT.', 'ΔU = n∫ CV(T)dT;  constant CV ⇒ ΔU = nCVΔT'),
      ], 'For a monatomic gas f = 3, CV = 3R/2, CP = 5R/2 and γ = 5/3.',
      'Classical active-mode counting fails when quantum levels freeze out. U = nCVT also contains a choice of additive energy constant.')

    P(20, 'refrigerator', 'Derive Carnot refrigerator performance', 'COPrev = Tc/(Th − Tc)',
      'Qc > 0: heat extracted from cold reservoir; Qh > 0: heat delivered to hot reservoir; Win > 0: work input.',
      'Cyclic refrigerator between two fixed-temperature reservoirs; reversibility for the maximum performance.', [
        ('Define the desired effect per cost', 'For a refrigerator the useful output is extracted cold-reservoir heat, and the required input is work.', 'COP ≡ Qc/Win'),
        ('Balance energy over the cycle', 'The working substance returns to its initial energy. Heat discharged equals heat removed plus supplied work.', 'Qh = Qc + Win'),
        ('Use the reversible heat ratio', 'A reversed Carnot engine has the same heat-magnitude ratio Qc/Qh = Tc/Th.', 'Qh = Qc Th/Tc', ('Why is the Carnot heat ratio universal?', 'clausius')),
        ('Eliminate heat magnitudes', 'Substitute the heat ratio in Win = Qh − Qc and divide Qc by the result.', 'COPrev = 1/(Th/Tc − 1) = Tc/(Th − Tc)'),
      ], 'For reservoirs at 270 K and 300 K, reversible COP is 9. Removing 900 J needs at least 100 J of input work in this ideal model.',
      'COP can exceed one because heat moved is not the same thing as work created. Temperatures must be absolute.')

    P(20, 'statistical-entropy', 'Derive multiplicity and the logarithmic entropy form', 'W = N!/(n₁!n₂!);  S = kB ln W',
      'W: number of allowed equal-probability microstates in a macrostate; N = n₁ + n₂: labelled particle count in a two-region counting model.',
      'Classical independent counting with equal accessible-state weights. Entropy additivity and monotonicity determine a logarithm up to its constant, fixed to kB by thermodynamic calibration.', [
        ('Choose which labels occupy the first region', 'Selecting n₁ particle labels from N is a binomial choice. Permutations within either region do not produce a new occupancy assignment.', 'W = binomial(N,n₁) = N!/[n₁!(N − n₁)!]'),
        ('Combine independent systems', 'Every state of A can pair with every state of B, so multiplicities multiply. Thermodynamic entropy is additive for independent systems.', 'WAB = WA WB;  SAB = SA + SB'),
        ('Solve the additivity requirement', 'A continuous increasing function with g(xy) = g(x) + g(y) has logarithmic form: set x = exp u and obtain an additive continuous function of u.', 'S(W) = C ln W + reference constant'),
        ('Fix the physical scale', 'Matching this statistical construction to reversible heat transfer on the absolute-temperature scale fixes C = kB. Equal a priori probabilities and the match to thermodynamics remain physical inputs.', 'S = kB ln W', ('Why does thermodynamic entropy use reversible heat over temperature?', 'entropy')),
      ], 'For four labelled particles with two in each half, W = 4!/(2!2!) = 6; placing all in one specified half gives W = 1.',
      'This simple position-counting model does not replace quantum indistinguishability or a complete phase-space entropy calculation.')

    P(22, 'charge-distributions', 'Derive point-charge, dipole and disk fields and potentials',
      'Edipole,axis ≈ 2kep/z³;  Edisk = σ[1 − z/√(z² + R²)]/(2ε₀);  Vdipole ≈ kep cos θ/r²',
      'ke = 1/(4πε₀); p = qd: dipole moment magnitude; R: disk radius; σ: uniform charge per area.',
      'Electrostatic vacuum fields; disk observation at z > 0; dipole approximations require observation distance much greater than separation d.', [
        ('Divide source force by test charge', 'Coulomb force on a test charge is proportional to that test charge. Division by it gives the point-source field; multiplying an external field by a probe charge reverses the definition.', '𝐄point = keQ r̂/r²;  𝐅probe = q𝐄external'),
        ('Subtract the two axial dipole fields', 'At z > d/2, the +q and −q axial fields oppose. Taylor expand the reciprocal squares for z ≫ d and retain the first nonzero term.', 'Eaxis = keq[(z − d/2)⁻² − (z + d/2)⁻²] ≈ 2keqd/z³'),
        ('Build the disk from rings', 'A ring of radius r and width dr has charge 2πσr dr. Insert this in the axial ring field and integrate r from zero to R.', 'Edisk = 2πkeσz ∫[0,R] r dr/(z² + r²)³ᐟ² = σ[1 − z/√(z² + R²)]/(2ε₀)'),
        ('Add potentials as scalars', 'Integrating field gives keq/r per point charge. Sum charges, or integrate dq, without vector projections.', 'V = Σkeqi/ri;  Vcontinuous = ke∫dq/r'),
        ('Expand a dipole potential', 'The distance difference to the two charges is approximately d cos θ at large r. Their reciprocal-distance difference is d cos θ/r².', 'Vdipole = keq(1/r₊ − 1/r₋) ≈ kep cos θ/r²'),
      ], 'Far from a finite disk its field tends to keQ/z² with Q = πR²σ; near a very large disk it approaches σ/(2ε₀).',
      'A dipole’s net charge vanishes, so its leading far potential and field fall faster than those of a point charge.')

    P(25, 'capacitor-geometries', 'Derive cylindrical and spherical capacitances',
      'Ccylinder = 2πεL/ln(b/a);  Csphere = 4πεab/(b − a);  Cisolated = 4πεR',
      'a < b: inner and outer radii; L: cylinder length; ε: uniform permittivity; Q: charge magnitude; ΔV: potential-difference magnitude.',
      'Coaxial long cylinders without end effects, or concentric spherical conductors; linear homogeneous dielectric.', [
        ('Find each gap field from symmetry', 'Gauss’s law on a coaxial cylinder gives Q/(2πεLr); a concentric sphere gives Q/(4πεr²).', 'Ecylinder = Q/(2πεLr);  Esphere = Q/(4πεr²)'),
        ('Integrate the cylindrical field', 'The potential-difference magnitude is the outward radial field integral between a and b.', 'ΔVcylinder = [Q/(2πεL)]∫[a,b]dr/r = Q ln(b/a)/(2πεL)'),
        ('Integrate the spherical field', 'The inverse-square integral gives a reciprocal-radius difference.', 'ΔVsphere = [Q/(4πε)](1/a − 1/b)'),
        ('Divide Q by each voltage', 'The charge cancels by the capacitance definition. For an isolated sphere, take b to infinity and replace a by R.', 'C = Q/ΔV;  b → ∞ ⇒ Cisolated = 4πεR'),
      ], 'A spherical capacitor with b = 2a has capacitance 8πεa, twice that of an isolated sphere of radius a in the same medium.',
      'Capacitance is defined between specified conductors and a reference; changing the environment changes that geometry problem.')

    P(25, 'capacitor-networks', 'Derive capacitor combinations and dielectric Gauss law',
      'Cparallel = ΣCi;  1/Cseries = Σ1/Ci;  ∮𝐃 · d𝐀 = Qfree',
      '𝐃 = ε₀𝐄 + 𝐏: electric displacement; 𝐏: polarization; ε = κε₀ for a uniform isotropic linear dielectric.',
      'Ideal capacitors, electrostatic lumped network, initially neutral isolated intermediate series nodes; stated linear dielectric relation where used.', [
        ('Sum parallel plate charges', 'Parallel capacitors share ΔV, while their charges add. Substitute Qi = CiΔV.', 'Qtotal = ΣCiΔV ⇒ Cparallel = ΣCi'),
        ('Sum series voltage differences', 'Neutral intermediate nodes force equal charge magnitudes Q on ideal series elements. Their voltages Qi/Ci add.', 'ΔVtotal = QΣ1/Ci ⇒ 1/Cseries = Σ1/Ci'),
        ('Separate free and bound charge', 'Polarization creates bound charge density ρbound = −∇·𝐏. Insert it into Gauss’s equation for total charge and collect terms.', '∇·(ε₀𝐄 + 𝐏) = ρfree'),
        ('Use the constitutive polarization model', 'For an isotropic linear material 𝐏 = ε₀(κ − 1)𝐄, so 𝐃 = κε₀𝐄. Integrating divergence gives the free-charge flux relation.', '∮κε₀𝐄 · d𝐀 = Qfree;  Cfilled = κCvacuum'),
      ], 'Two 10 μF capacitors give 20 μF in parallel and 5 μF in series under the ideal-network assumptions.',
      'A spatially varying dielectric cannot in general be replaced by one scalar κ multiplying the entire answer.')

    P(26, 'current-flux', 'Derive current as charge flux and local continuity', 'I = ∫𝐉 · d𝐀;  ∂ρcharge/∂t + ∇·𝐉 = 0',
      'ρcharge: volume charge density; 𝐮: carrier velocity; 𝐉 = ρcharge𝐮 for one continuous carrier flow; n: carrier number density.',
      'A specified oriented surface, macroscopic smooth charge flow; sum species contributions if several charge types move.', [
        ('Count crossing volume', 'Across a small oriented area dA, the volume swept per time is the normal velocity component times dA.', 'dVcross/dt = 𝐮 · d𝐀'),
        ('Multiply by charge density', 'Charge carried by that volume is density times volume. This identifies local current density.', 'dI = ρcharge𝐮 · d𝐀 = 𝐉 · d𝐀'),
        ('Integrate over the surface', 'Add contributions using the chosen normal. For a uniform perpendicular flow, I = JA.', 'I = ∫surface 𝐉 · d𝐀'),
        ('Conserve charge within a volume', 'Outward current removes enclosed charge. Applying the divergence theorem to this balance gives the local continuity equation.', 'dQinside/dt = −∮𝐉 · d𝐀 ⇒ ∂ρcharge/∂t = −∇·𝐉'),
      ], 'If a uniform J = 10⁶ A/m² is normal to a 10⁻⁶ m² wire cross section, current is 1 A.',
      'Current is a signed surface flux; current density is a vector. Electrical resistivity and charge density often share a rho symbol but have different units.')

    P(27, 'battery-discharge', 'Derive terminal voltage, battery power and RC discharge',
      'I = ℰ/(R + r);  Vterminal = ℰ − Ir;  qdischarge = q₀ exp(−t/(RC))',
      'ℰ: source emf; r: internal series resistance; R: external resistance; q: signed capacitor plate charge.',
      'Ideal source plus internal ohmic resistance; separate RC discharge through a resistor with the source disconnected.', [
        ('Balance source rise and series drops', 'The loop contains drops IR and Ir. Rearrange the zero loop sum for current and the external terminal voltage.', 'ℰ − I(R + r) = 0;  Vterminal = IR = ℰ − Ir'),
        ('Multiply by current', 'The chemical power is emf times current. Internal resistive heating accounts for the difference between chemical power and power delivered at the terminals.', 'ℰI = I²r + Vterminal I'),
        ('Remove the source in the RC loop', 'Using current into the chosen positive capacitor plate as dq/dt gives a negative charging-direction current during discharge.', 'R dq/dt + q/C = 0'),
        ('Integrate the homogeneous equation', 'Separate dq/q = −dt/(RC) and impose initial charge q₀. Differentiate to obtain signed current.', 'q = q₀ exp(−t/(RC));  I = −q₀ exp(−t/(RC))/(RC)'),
      ], 'A 12 V emf with r = 1 Ω and external R = 5 Ω supplies 2 A and has terminal voltage 10 V.',
      'A charging battery has different current direction; keep a signed loop convention instead of blindly subtracting Ir.')

    P(29, 'magnetic-geometries', 'Derive arc, toroid, dipole fields and wire forces',
      'Barc = μ₀Iφ/(4πR);  Btoroid = μ₀NI/(2πr);  F/L = μ₀I₁I₂/(2πd)',
      'R,φ: circular-arc radius and angle in radians; N: toroid turns; d: parallel-wire separation; μ: loop dipole moment.',
      'Magnetostatics in vacuum; ideal tightly wound toroid; long thin wires; dipole approximation only far from the loop.', [
        ('Integrate Biot–Savart around an arc', 'Every arc element is perpendicular to the radius and contributes in the same axial direction at the centre. Use ds = R dφ.', 'B = [μ₀I/(4πR²)]∫ds = μ₀Iφ/(4πR)'),
        ('Apply Ampère’s law inside a toroid', 'A circular path within the winding encloses NI and has constant tangential B by ideal symmetry.', 'B(2πr) = μ₀NI ⇒ B = μ₀NI/(2πr)'),
        ('Use one wire’s field on the other wire', 'At separation d the first wire’s field is μ₀I₁/(2πd). Multiply by I₂L for a perpendicular current–field angle.', 'F = I₂LB₁ = μ₀LI₁I₂/(2πd)'),
        ('Integrate a loop’s axial field', 'On the loop axis, transverse components cancel. Biot–Savart gives Bz = μ₀IR²/[2(R² + z²)³ᐟ²]. For z ≫ R substitute μ = IπR².', 'Bz,far ≈ μ₀μ/(2πz³)'),
      ], 'For a full circle φ = 2π, the central arc formula reduces to B = μ₀I/(2R).',
      'Parallel currents attract for the same current direction; opposite directions repel. Use vector directions before interpreting a signed force.')

    P(30, 'rl-mutual', 'Derive RL transients, mutual emf and magnetic energy density',
      'Irise = (ℰ/R)[1 − exp(−Rt/L)];  Idecay = I₀ exp(−Rt/L);  uB = B²/(2μ₀)',
      'L: constant self-inductance; M: mutual inductance; n: solenoid turns per length; A: solenoid cross section.',
      'Linear inductors, fixed coil geometry, vacuum solenoid well away from ends, and lumped resistor–inductor circuit.', [
        ('Write and solve the RL loop', 'A constant source satisfies LdI/dt + RI = ℰ. Its steady solution is ℰ/R and its homogeneous solution decays at rate R/L.', 'I(t) = ℰ/R + [I(0) − ℰ/R]exp(−Rt/L)'),
        ('Remove the source', 'With ℰ = 0 the same homogeneous solution gives current decay. Initial current sets its amplitude.', 'I(t) = I₀ exp(−t/τL);  τL = L/R'),
        ('Find a solenoid’s inductance', 'Its field is μ₀nI, each turn links BA, and total turns are nℓ. Divide total flux linkage by current.', 'L = (nℓ)(μ₀nI)A/I = μ₀n²Aℓ'),
        ('Divide stored energy by field volume', 'Insert the solenoid inductance in U = LI²/2 and divide by Aℓ. Replace μ₀nI by B.', 'uB = ½μ₀n²I² = B²/(2μ₀)'),
        ('Differentiate mutual linkage', 'Define N₂Φ₂from₁ = MI₁. Faraday’s law differentiates it to the emf in coil 2; reciprocity gives the analogous coil-1 relation for a reciprocal linear medium.', 'ℰ₂ = −M dI₁/dt;  ℰ₁ = −M dI₂/dt'),
      ], 'A 0.2 H inductor with R = 10 Ω has current-decay time constant 0.020 s.',
      'The magnetic energy-density formula shown is the vacuum linear case; nonlinear magnetic media need a more general energy integral.')

    P(31, 'ac-power-transformers', 'Derive RLC damping, AC power and transformer ratios',
      'Pavg = Irms²R = VrmsIrms cos φ;  Vs/Vp = Ns/Np;  Req = (Np/Ns)²Rload',
      'φ: voltage phase ahead of current; Np,Ns: turns; Vrms,Irms: RMS quantities; Q: initial charge amplitude.',
      'Sinusoidal steady AC or underdamped free RLC motion; ideal transformer with common flux, no losses and negligible magnetizing current.', [
        ('Include a resistor in free LC motion', 'The loop equation gains a term Rq̇. Its characteristic roots follow exactly the damped-oscillator quadratic with m→L, b→R, k→1/C.', 'Lq̈ + Rq̇ + q/C = 0;  q = Qexp(−Rt/(2L))cos(ω′t + φ);  ω′² = 1/(LC) − R²/(4L²)'),
        ('Average instantaneous AC power', 'For v = Vmax cos ωt and i = Imax cos(ωt − φ), the product-to-sum identity leaves mean VmaxImax cos φ/2. RMS conversion divides each peak by √2.', 'Pavg = VrmsIrms cos φ = Irms²R'),
        ('Read phase from the impedance triangle', 'The quadrature voltage is I(XL − XC) and the in-phase voltage is IR. Their ratio is tan φ.', 'tan φ = (ωL − 1/(ωC))/R'),
        ('Use common changing flux', 'Faraday’s law gives winding voltage proportional to turn count if both windings link the same flux. Thus the voltage ratio is the turns ratio.', 'Vp/Np = Vs/Ns = |dΦ/dt|'),
        ('Conserve ideal transformer power', 'Equality of input and output power gives the inverse current ratio. Divide primary voltage by primary current and substitute the two ratios.', 'Is/Ip = Np/Ns;  Vp/Ip = (Np/Ns)²(Vs/Is)'),
      ], 'A 2:1 primary-to-secondary turns ratio halves voltage, doubles ideal load current relative to primary load current, and reflects a load resistance multiplied by four.',
      'Peak and RMS ratios match for sinusoids, but average power requires RMS or the appropriate explicit factor one half.')

    P(32, 'magnetic-moments', 'Derive orbital and spin magnetic-moment consequences',
      '𝛍orb = −e𝐋/(2m);  𝛍spin ≈ −e𝐒/m;  Fz = μz ∂B/∂z',
      'μB = eℏ/(2m): Bohr magneton; 𝐋: orbital angular momentum; 𝐒: intrinsic spin; m: electron mass.',
      'Nonrelativistic electron orbital motion and leading gspin = 2 approximation; slowly varying external magnetic field with a specified moment orientation.', [
        ('Model a circulating charge', 'An orbiting charge q completes one circuit per period 2πr/v, giving I = qv/(2πr) and magnetic moment Iπr². Compare with orbital angular momentum mrv.', 'μorb/L = q/(2m) ⇒ 𝛍orb = −e𝐋/(2m)'),
        ('State the independent spin input', 'Spin is intrinsic, not a literal charged rotating ball. Quantum theory supplies spin ½ and a leading gyromagnetic factor 2; more precise g differs slightly from 2.', '𝛍spin = −g(e/(2m))𝐒,  g ≈ 2'),
        ('Insert quantized projections', 'Using Lz = mℓℏ and Sz = msℏ gives the measured moment components in multiples of the Bohr magneton.', 'μorb,z = −mℓμB;  μspin,z ≈ −2msμB,  ms = ±½'),
        ('Differentiate orientation energy', 'For a fixed moment, U = −μzB(z). Force is minus its spatial derivative. The two orientations ±|μz| have energies separated by 2|μz|B.', 'Fz = μz∂B/∂z;  ΔE = 2|μz|B;  hfresonance = ΔE'),
      ], 'A spin-½ moment in a uniform field has two projection-dependent energies, while a field gradient can separate the corresponding beam components.',
      'The proton has a different gyromagnetic ratio. Do not substitute the electron Bohr magneton for a nuclear magnetic moment.')

    P(32, 'curie-law', 'Derive Curie’s law in the weak-field dipole model', 'M ≈ nμ²B/(3kBT)',
      'n: dipoles per volume; μ: permanent dipole magnitude; M: magnetization; θ: angle between dipole and field; b = μB/(kBT).',
      'Independent classical dipoles in equilibrium with weak field b ≪ 1. Quantum dipoles change the coefficient; interacting ferromagnets need a different theory.', [
        ('Define magnetization', 'Add the magnetic moments and divide by sample volume. Complete alignment gives Mmax = nμ.', '𝐌 ≡ (Σ𝛍i)/V'),
        ('Weight orientation energy', 'The dipole energy is −μB cos θ, so the equilibrium orientation weight is exp(b cos θ). Spherical orientation counting contributes sin θ dθ.', '⟨cos θ⟩ = [∫[−1,1] u exp(bu)du]/[∫[−1,1] exp(bu)du]'),
        ('Expand the weak-field weights', 'Replace exp(bu) by 1 + bu. The odd integral in the numerator vanishes, leaving b∫u²du = 2b/3; the denominator is approximately 2.', '⟨cos θ⟩ ≈ b/3'),
        ('Multiply by dipole density', 'The aligned average component is μ⟨cos θ⟩ per dipole. This yields M = CB/T with classical C = nμ²/(3kB).', 'M = nμ⟨cos θ⟩ ≈ nμ²B/(3kBT)'),
      ], 'At fixed weak B, doubling absolute temperature halves this model’s magnetization.',
      'Curie’s constant depends on microscopic moments and quantum state counting; the classical coefficient is not universal.')

    P(33, 'polarization-refraction', 'Derive Malus’s law, Snell’s law and special angles',
      'I = I₀cos²θ;  n₁sin θ₁ = n₂sin θ₂;  sin θc = n₂/n₁;  tan θB = n₂/n₁',
      'θ: angle between polarization and transmission axis; ni: refractive indices; θi: ray angles from boundary normal.',
      'Ideal polarizer, stationary plane interface, isotropic transparent media; critical angle requires n₁ > n₂; Brewster formula assumes nonmagnetic dielectrics.', [
        ('Project the incident electric amplitude', 'An ideal polarizer transmits the field component along its transmission direction. Intensity scales as amplitude squared.', 'Etransmitted = E₀cos θ ⇒ I = I₀cos²θ'),
        ('Average random polarization', 'Unpolarized light has uniformly distributed polarization directions. The average cos²θ is ½.', 'Iunpolarized,out = I₀/2'),
        ('Match phase along an interface', 'All points on a stationary boundary must share the same tangential phase and time frequency. Thus tangential wavenumbers match; with k = nω/c this gives refraction.', 'k₁sin θ₁ = k₂sin θ₂ ⇒ n₁sin θ₁ = n₂sin θ₂'),
        ('Set the grazing transmitted angle', 'At the limit θ₂ = 90°, Snell’s law gives the critical angle. Frequency remains unchanged while medium speed becomes c/n, so wavelength becomes λ₀/n.', 'sin θc = n₂/n₁;  λmedium = λ₀/n'),
        ('Cancel the parallel reflected field', 'For nonmagnetic dielectrics the parallel-polarization Fresnel numerator is n₂cos θ₁ − n₁cos θ₂. Setting it to zero together with Snell’s law gives θ₁ + θ₂ = 90° and tan θB = n₂/n₁.', 'rp = (n₂cos θ₁ − n₁cos θ₂)/(n₂cos θ₁ + n₁cos θ₂);  rp(θB) = 0'),
      ], 'An ideal polarizer crossed by 60° to already polarized light transmits one quarter of its incident intensity.',
      'Brewster’s formula depends on the electromagnetic boundary conditions, not Snell’s law alone.')

    P(34, 'refracting-instruments', 'Derive spherical refraction, lensmaker and instrument magnification',
      'n₁/p + n₂/i = (n₂ − n₁)/R;  1/f = (n − 1)(1/R₁ − 1/R₂)',
      'p: real object distance; i: real image distance; R: signed surface radius; D: chosen near-point reference; fob,fey: objective and eyepiece focal lengths.',
      'Paraxial rays, thin lens in air, signed radii positive when the centre is on the outgoing side. Magnifier formulas use relaxed-eye viewing.', [
        ('Linearize refraction geometry', 'For a ray at height h, its small object and image angles are h/p and h/i, while the surface normal tilts h/R. Linearized Snell gives n₁(h/p + h/R) = n₂(h/R − h/i).', 'n₁/p + n₂/i = (n₂ − n₁)/R'),
        ('Apply refraction twice', 'For a thin lens, the first image is the second surface’s virtual object. Add the two surface equations so that the internal image-distance terms cancel.', '1/p + 1/i = (n − 1)(1/R₁ − 1/R₂) = 1/f'),
        ('Compare central-ray triangles', 'The image height divided by object height is the signed ray-slope ratio. The height-ratio definition becomes a distance ratio.', 'm ≡ hi/ho = −i/p'),
        ('Compare angular sizes for a magnifier', 'A naked-eye object at reference distance D subtends approximately h/D. At a magnifier focus it subtends h/f while the emerging light is parallel.', 'mθ ≈ (h/f)/(h/D) = D/f'),
        ('Combine objective and eyepiece', 'A microscope objective gives approximately −s/fob lateral magnification, followed by D/fey angular magnification. A telescope’s focal-plane image height is fobθin, so θout ≈ −fobθin/fey.', 'Mmicroscope ≈ −(s/fob)(D/fey);  mtelescope = −fob/fey'),
      ], 'A relaxed-eye magnifier with f = 5 cm and conventional D = 25 cm has angular magnification 5.',
      'The 25 cm reference is a viewing convention, not a fundamental constant; finite-distance viewing changes the magnifier formula.')

    P(36, 'apertures-bragg', 'Derive circular diffraction, two-slit envelopes and Bragg angles',
      'sin θfirst = 1.22λ/D;  Idouble ∝ cos²β (sin α/α)²;  2d sin θ = mλ',
      'D: circular aperture diameter; d: crystal-plane separation for Bragg diffraction; α,β: single-slit and slit-separation phase parameters.',
      'Scalar far-field diffraction with uniform illumination; circular pupil; coherent equivalent crystal planes; small angle for Rayleigh’s θ ≈ 1.22λ/D.', [
        ('Integrate a circular pupil', 'The far-field amplitude is the two-dimensional Fourier integral of the aperture. Polar coordinates reduce the angular integral to 2πJ₀, and integrating radius gives 2J₁(u)/u.', 'E(θ)/E(0) = 2J₁(u)/u;  u = πD sin θ/λ'),
        ('Locate the first zero', 'The first positive numerical root of J₁ is 3.831706. Divide by π to obtain the factor approximately 1.21967.', 'sin θfirst = (3.831706/π)λ/D ≈ 1.22λ/D'),
        ('Apply a resolution convention', 'Rayleigh’s criterion places one source’s central maximum at the other’s first minimum. With small θ, angular separation is approximately 1.22λ/D.', 'θRayleigh ≈ 1.22λ/D'),
        ('Translate and add two finite slits', 'Each slit has the same sinc amplitude envelope. Translating a slit shifts phase; summing the two phases multiplies that envelope by 2cos β. Squaring yields the product pattern.', 'I(θ) = Icentral cos²β (sin α/α)²'),
        ('Count paths between crystal planes', 'A ray reflecting from the next plane down travels extra distance d sin θ on the incoming leg and again on the outgoing leg. Constructive phase requires a total integer wavelength.', 'Δpath = 2d sin θ = mλ'),
      ], 'An aperture twice as wide halves the small-angle Rayleigh limit at a fixed wavelength.',
      'The numerical factor 1.22 comes from a circular-aperture wave integral; it is neither a universal aperture constant nor an empirical fit.')

    P(37, 'lorentz-transform', 'Derive the Lorentz transform, length contraction and velocity addition',
      'x′ = γ(x − vt);  t′ = γ(t − vx/c²);  u = (u′ + v)/(1 + u′v/c²)',
      'v: frame S′ speed relative to S; γ = 1/√(1 − v²/c²); primed and unprimed coordinates refer to the same event.',
      'Special-relativistic inertial frames, aligned axes, origins coincident at t = 0, homogeneity and isotropy.', [
        ('Use linearity and the moving origin', 'Homogeneity makes inertial coordinate transformations linear. Since x′ = 0 follows x = vt, write x′ = A(x − vt). Requiring both light rays x = ±ct to satisfy x′ = ±ct′ fixes t′ = A(t − vx/c²).', 'x′ = A(x − vt);  t′ = A(t − vx/c²)'),
        ('Impose inverse-frame reciprocity', 'The inverse has speed −v and the same scale A by isotropy. Substituting transformations gives A²(1 − v²/c²) = 1. Choose positive A continuously connected to v = 0.', 'A = γ;  y′ = y;  z′ = z'),
        ('Measure moving endpoints simultaneously', 'An object at rest in S′ has proper length Δx′ = L₀. The S measurement requires Δt = 0; hence Δx′ = γΔx.', 'L = Δx = L₀/γ'),
        ('Divide coordinate differentials', 'Use the inverse transform dx = γ(dx′ + vdt′) and dt = γ(dt′ + vdx′/c²). Their ratio gives longitudinal velocity addition.', 'u = dx/dt = (u′ + v)/(1 + u′v/c²)'),
      ], 'Combining u′ = 0.8c and v = 0.8c gives u ≈ 0.976c, below c.',
      'Length measurements require simultaneous endpoint events in the measuring frame. Time and position cannot be transformed independently.')

    P(37, 'light-doppler', 'Derive longitudinal and transverse light Doppler shifts',
      'λreceding/λ₀ = √[(1 + β)/(1 − β)];  ftransverse = f₀/γ',
      'β = v/c; f₀,λ₀: source-rest frequency and wavelength; θ: photon direction relative to source velocity in detector frame.',
      'Inertial source and detector in vacuum; transverse formula uses a photon arriving perpendicular to source velocity in the detector frame.', [
        ('Transform successive wave phases', 'Wave phase is invariant between inertial frames. Its coefficients form a four-vector, so the source-frame angular frequency obeys ω₀ = γ(ω − vkx).', 'ω₀ = γω(1 − βcos θ)'),
        ('Choose a receding source', 'For light travelling opposite the source velocity, cos θ = −1. Then f = f₀/[γ(1 + β)]. The reciprocal frequency ratio is the wavelength ratio.', 'λ/λ₀ = γ(1 + β) = √[(1 + β)/(1 − β)]'),
        ('Take the slow-speed limit', 'For |β| ≪ 1, expand the square-root ratio to 1 + β at first order. The fractional wavelength shift then approximates the radial speed divided by c.', '|Δλ|/λ₀ ≈ |v|/c'),
        ('Choose a transverse arriving ray', 'Set cos θ = 0 in the frequency transform. The remaining time-dilation factor gives the transverse shift.', 'f = f₀/γ = f₀√(1 − β²)'),
      ], 'At recession speed 0.6c, λ/λ₀ = 2. At detector-frame transverse observation, f/f₀ = 0.8.',
      'The angle is frame-dependent. State in which frame the direction is transverse; sound’s medium-based formula is different.')

    P(38, 'planck-radiation', 'Derive Planck radiation, Wien’s maximum and the T⁴ law',
      'Mλ = [2πhc²/λ⁵]/[exp(hc/(λkBT)) − 1];  M = σT⁴',
      'Mλ: hemispherical blackbody power per area per wavelength; ν: frequency; x = hν/(kBT); ε: grey emissivity.',
      'Equilibrium photon modes in a large cavity, two polarizations, zero photon chemical potential, ideal blackbody or a stated grey-surface approximation.', [
        ('Count photon modes and their mean energy', 'Counting wavevectors with two polarizations gives 8πν²/c³ modes per volume per frequency. Boson thermal occupancy is 1/[exp(hν/(kBT)) − 1]. Multiply by hν.', 'uν = (8πhν³/c³)/[exp(hν/(kBT)) − 1]'),
        ('Convert cavity density to outward emission', 'For an isotropic cavity, integrating the normal velocity over an outward hemisphere yields flux cuν/4. Changing variable ν = c/λ supplies |dν/dλ| = c/λ².', 'Mλ = (c/4)uν |dν/dλ| = [2πhc²/λ⁵]/[exp(hc/(λkBT)) − 1]'),
        ('Maximize with respect to wavelength', 'Set the derivative of ln Mλ to zero. With x = hc/(λkBT), the nonzero root solves 5(1 − exp(−x)) = x, giving x ≈ 4.965114.', 'λmaxT = hc/(4.965114kB) ≈ 2.898 × 10⁻³ m·K'),
        ('Integrate over all frequencies', 'Change variable to x. Expand 1/(ex − 1) as Σ exp(−nx); the integral of x³exp(−nx) is 6/n⁴. Summing gives π⁴/15.', 'M = [2πkB⁴T⁴/(h³c²)]∫[0,∞] x³/(ex − 1)dx = [2π⁵kB⁴/(15h³c²)]T⁴'),
        ('Apply a grey-surface model', 'Define σ by the preceding constant. A surface of area A and frequency-independent effective emissivity ε emits εAσT⁴; a large isotropic environment at Tenv supplies absorption εAσTenv⁴ under the grey equilibrium assumptions.', 'Pnet,out = εAσ(T⁴ − Tenv⁴)'),
      ], 'Doubling blackbody absolute temperature multiplies total emitted power per area by 16 and halves the peak wavelength.',
      'A peak per unit wavelength is not the same location as a peak per unit frequency; converting spectral variables changes the density.')

    P(38, 'quantum-foundations', 'Schrödinger dynamics, matter waves and the uncertainty bound',
      'iℏ∂Ψ/∂t = ĤΨ;  ΔxΔpx ≥ ℏ/2;  λ = h/p',
      'Ψ: wavefunction; Ĥ: Hamiltonian operator; px = −iℏ∂/∂x; Δ: standard deviation, not instrument error.',
      'Nonrelativistic quantum mechanics with normalized states and suitable differentiability and boundary decay. The dynamics and operator assignments are explicit quantum inputs.', [
        ('State the quantum dynamical input', 'For a particle, kinetic energy is represented by −ℏ²∇²/(2m), and potential energy by multiplication by U. The time-dependent Schrödinger equation is a foundational model equation.', 'Ĥ = −ℏ²∇²/(2m) + U'),
        ('Separate a stationary state', 'Insert Ψ(x,t) = ψ(x)exp(−iEt/ℏ). The common time factor cancels, giving the one-dimensional stationary equation.', '−ℏ²ψ″/(2m) + Uψ = Eψ'),
        ('Apply momentum to a plane wave', 'A plane wave exp(ikx) is a momentum eigenstate: applying −iℏ∂x returns ℏk times the same state. Since one wavelength advances phase by 2π, p = ℏk = h/λ.', 'p = ℏk;  λ = 2π/k ⇒ λ = h/p'),
        ('Use the commutator uncertainty theorem', 'Cauchy–Schwarz applied to (x − ⟨x⟩)Ψ and (px − ⟨px⟩)Ψ yields ΔxΔpx ≥ |⟨[x,px]⟩|/2. Direct differentiation gives [x,px]Ψ = iℏΨ.', 'ΔxΔpx ≥ ½|iℏ| = ℏ/2'),
        ('Conserve scattering probability', 'For a real stationary potential the probability current is constant. An incoming particle is either reflected or transmitted; dividing the two outgoing currents by the incoming current makes their fractions add to one.', 'R + T = 1 ⇒ T = 1 − R'),
      ], 'A Gaussian can attain the precise standard-deviation bound ℏ/2. A rough order-of-magnitude statement often suppresses this factor.',
      'The textbook uses an order-scale uncertainty expression. For standard deviations the rigorous lower bound is ℏ/2, not ℏ.')

    P(39, 'quantum-normalization', 'Derive wavefunction normalization and multidimensional box states',
      'ψn = √(2/L)sin(nπx/L);  Enx,ny = h²(nx²/Lx² + ny²/Ly²)/(8m)',
      'ψ: spatial state; |ψ|²: probability density by the Born rule; n: positive box mode integer; P(r): radial probability density.',
      'Born probability rule, infinite rectangular walls for the separated box states, and normalized angular states for radial probability.', [
        ('State the probability rule', 'Quantum mechanics supplies |ψ|² as probability density. Total probability one imposes normalization; probabilities on subregions follow by integrating that density.', '∫all space |ψ|²dV = 1'),
        ('Normalize a one-dimensional box mode', 'For ψ = A sin(nπx/L), the sine squared integrates to L/2 for positive integer n. Solve |A|²L/2 = 1.', 'A = √(2/L)'),
        ('Separate independent directions', 'The rectangular Hamiltonian is Hx + Hy and its eigenfunction can be a product X(x)Y(y). Normalization factors multiply while the energy eigenvalues add.', 'ψnx,ny = ψnx(x)ψny(y);  E = Ex + Ey'),
        ('Count spherical shell probability', 'With ψ = R(r)Y(θ,φ) and normalized Y, volume measure r²dr dΩ gives radial density r²|R(r)|².', 'P(r) = r²|R(r)|²;  Prob(r₁ < r < r₂) = ∫[r₁,r₂] P(r)dr'),
      ], 'The normalized first box state has probability 1/2 in either half of the symmetric well.',
      'ψ itself is not a probability density. For complex wavefunctions use |ψ|², not ψ².')

    P(40, 'quantum-angular', 'Derive angular-momentum eigenvalues and magnetic projections',
      'L² = ℓ(ℓ + 1)ℏ²;  Lz = mℓℏ;  S² = s(s + 1)ℏ²',
      'ℓ: orbital angular-momentum index; mℓ: projection index; s = ½: electron spin input; J± = Jx ± iJy: ladder operators.',
      'Quantum angular-momentum commutators [Ji,Jj] = iℏεijkJk and normalized eigenstates. Orbital single-valuedness gives integer ℓ; intrinsic spin can be half-integer.', [
        ('Start from the angular-momentum algebra', 'Choose simultaneous eigenstates of J² and Jz. The commutator [Jz,J±] = ±ℏJ± means a ladder step changes projection by exactly ℏ.', 'Jz|j,m⟩ = mℏ|j,m⟩'),
        ('Stop the upward ladder', 'At its highest state, J+ annihilates it. The identity J−J+ = J² − Jz² − ℏJz then fixes the squared-magnitude eigenvalue.', 'J² = j(j + 1)ℏ²'),
        ('Stop the downward ladder', 'The corresponding lower endpoint is m = −j, and unit steps run to +j. For orbital wavefunctions, periodic azimuthal dependence requires integer m and integer ℓ.', 'm = −j, −j + 1, …, j;  orbital ℓ = 0,1,2,…'),
        ('Insert the gyromagnetic relation', 'The orbital moment is −e𝐋/(2m), so its magnitude and projections follow by substitution. The electron spin value s = ½ is a physical species input, not a consequence of orbital motion.', '|μorb| = μB√[ℓ(ℓ + 1)];  μorb,z = −mℓμB;  μspin,z ≈ −2msμB'),
        ('Restrict a hydrogen shell', 'For the Coulomb bound states the radial solution gives n = nr + ℓ + 1 with a nonnegative radial integer nr. Therefore a shell of principal index n permits ℓ from zero through n − 1.', 'ℓ = 0, 1, …, n − 1', ('Why does the radial solution impose this restriction?', 'hydrogen-quantum')),
      ], 'An ℓ = 1 orbital state has magnitude √2ℏ and possible z projections −ℏ, 0 and +ℏ.',
      'The Bohr-orbit rule L = nℏ is a historical model postulate, not the modern orbital-angular-momentum spectrum.')

    P(41, 'electron-gas-states', 'Derive the electron density of states and Fermi energy',
      'g(E) = (8√2πm³ᐟ²/h³)√E;  EF = ℏ²(3π²n)²ᐟ³/(2m)',
      'V: sample volume; n: conduction electrons per volume; k: wavevector magnitude; g(E): states per volume per energy including two spins.',
      'Three-dimensional free-electron box model with two spin states; zero temperature for EF; band-effective parameters require a suitable band model.', [
        ('Count wavevector cells', 'Periodic boundaries give one k state per volume (2π)³/V. Two spin states and a spherical shell of area 4πk² yield dN/V = k²dk/π².', 'Nstates(k)/V = k³/(3π²)'),
        ('Change variable from k to energy', 'For nonrelativistic free electrons E = ℏ²k²/(2m). Differentiate the state count with respect to E.', 'g(E) = (1/(2π²))(2m/ℏ²)³ᐟ²√E'),
        ('Fill states at zero temperature', 'Each state below EF is occupied and each above is empty. Integrating g from zero to EF gives n.', 'n = (1/(3π²))(2mEF/ℏ²)³ᐟ² ⇒ EF = ℏ²(3π²n)²ᐟ³/(2m)'),
        ('Use thermal occupation at nonzero temperature', 'Multiply available-state density by Fermi–Dirac occupation to get occupied-state density. The integral of the product gives electron number density.', 'goccupied(E) = g(E)f(E);  n = ∫ g(E)f(E)dE', ('Derive Fermi–Dirac occupation', 'fermi-dirac')),
        ('Count carriers or relate a gap to light', 'If each atom contributes z mobile electrons, use atom count ρmassVNA/Mmol. A direct radiative transition of energy Eg emits a photon hc/λ = Eg in the simple gap model.', 'n = zρmassNA/Mmol;  λ ≈ hc/Eg'),
      ], 'At zero temperature doubling n increases this free-electron EF by 2²ᐟ³, about 1.59.',
      'Available states and occupied states differ. A band-gap photon estimate also needs the relevant optical transition and material conditions.')

    P(42, 'nuclear-size-fusion', 'Derive nuclear radius scaling and a fusion confinement criterion',
      'R = r₀A¹ᐟ³;  nτ ≳ 12kBT/(⟨σv⟩Eα)  (idealized D–T self-heating)',
      'A: nucleon count; n: total ion density with nD = nT = n/2; τ: energy-confinement time; Eα: alpha heating per D–T reaction.',
      'Approximately constant nuclear matter density for radius scaling; equal-temperature quasineutral D–T plasma, simple energy balance without radiative losses for the illustrative confinement estimate.', [
        ('Assume approximately constant nuclear density', 'Nuclear volume is proportional to nucleon number. A spherical volume then makes radius proportional to the cube root of A. The fitted coefficient r₀ is empirical.', '4πR³/3 = A vnucleon ⇒ R = [3vnucleon/(4π)]¹ᐟ³ A¹ᐟ³'),
        ('Count fusion reactions per volume per time', 'For two distinct reactant species, the thermally averaged reaction rate is nDnT⟨σv⟩. With equal fractions this is n²⟨σv⟩/4.', 'Palpha/volume = (n²/4)⟨σv⟩Eα'),
        ('Count thermal energy to be retained', 'For equal ion and electron temperatures with electron density n, both populations contribute 3nkBT/2, so total thermal energy density is 3nkBT.', 'Ploss/volume = 3nkBT/τ'),
        ('Require heating to meet losses', 'Set alpha heating at least equal to the simplified loss rate and cancel one density factor. The threshold depends on temperature through both T and the reactivity.', 'nτ ≥ 12kBT/(⟨σv⟩Eα)'),
      ], 'Radius scaling predicts that increasing nucleon number by eight approximately doubles nuclear radius.',
      'A fixed numerical Lawson threshold is not fundamental or universal. Fuel choice, temperature, losses and the definition of confinement determine it.')

    P(39, 'hydrogen-quantum', 'Derive hydrogen energies from the radial Schrödinger equation',
      'En = −μ(kee²)²/(2ℏ²n²);  n = nr + ℓ + 1',
      'μ: electron–proton reduced mass; ke = 1/(4πε₀); a₀ = ℏ²/(μkee²); κ = √(−2μE)/ℏ for a bound state.',
      'Nonrelativistic Coulomb potential, no fine structure or radiative corrections, normalizable stationary states with E < 0.', [
        ('Separate radial and angular motion', 'Insert ψ = R(r)Yℓm into the three-dimensional Schrödinger equation and use the angular eigenvalue ℓ(ℓ + 1)ℏ². Setting u = rR removes the first radial derivative.', 'u″ + [−κ² + 2/(a₀r) − ℓ(ℓ + 1)/r²]u = 0', ('What physical equation is being solved?', 'quantum-foundations')),
        ('Factor the required endpoint behaviour', 'Regularity at zero requires u proportional to r^(ℓ + 1); decay at infinity requires exp(−κr). Set u = r^(ℓ + 1)exp(−κr)F(ρ) with ρ = 2κr and substitute.', 'ρF″ + (2ℓ + 2 − ρ)F′ + [1/(κa₀) − ℓ − 1]F = 0'),
        ('Terminate the series to preserve normalization', 'A power series F = Σajρʲ has recursion a(j+1)/aj = [j + ℓ + 1 − 1/(κa₀)]/[(j + 1)(j + 2ℓ + 2)]. A nonterminating regular solution grows too fast at infinity. Termination at j = nr requires its numerator to vanish.', '1/(κa₀) = nr + ℓ + 1 ≡ n'),
        ('Convert decay scale to energy', 'Substitute κ = 1/(na₀) into E = −ℏ²κ²/(2μ), then substitute the definition of a₀. This produces the energy spectrum without literal Bohr orbits.', 'En = −ℏ²/(2μa₀²n²) = −μ(kee²)²/(2ℏ²n²)'),
      ], 'Replacing μ by the electron mass gives the fixed-proton approximation En ≈ −13.6 eV/n². Reduced mass gives the leading finite-proton-mass correction.',
      'The principal integer n comes from radial regularity and normalizability. It does not assert angular momentum nℏ.')

    P(19, 'boltzmann-weights', 'Derive Boltzmann weights from a thermal reservoir',
      'Pi ∝ exp(−Ei/(kBT));  wi,N ∝ exp[−(Ei − μN)/(kBT)]',
      'Ωbath: reservoir multiplicity; Sbath = kB ln Ωbath; T: reservoir temperature; μ: chemical potential; Z: sum of statistical weights.',
      'Weak coupling, a large equilibrium reservoir, equal a priori weights for accessible microstates of the isolated total, and negligible reservoir temperature change.', [
        ('State the statistical starting postulate', 'Accessible microstates of an isolated equilibrium total are assigned equal probabilities. A subsystem state is more probable when more reservoir states can accompany it.', 'Ptotal,micro = 1/Ωtotal'),
        ('Count reservoir partners', 'If the subsystem has energy Ei, its reservoir has remaining energy Etotal − Ei. Thus subsystem-state probability is proportional to that reservoir multiplicity.', 'Pi ∝ Ωbath(Etotal − Ei)'),
        ('Expand the reservoir entropy', 'For a fixed-volume, fixed-particle reservoir, reversible first-law changes obey dUbath = T dSbath; hence ∂Sbath/∂Ubath = 1/T. A first-order Taylor expansion gives Sbath(Etotal − Ei) ≈ S₀ − Ei/T.', 'ln Ωbath(Etotal − Ei) ≈ S₀/kB − Ei/(kBT)', ('Why does entropy relate reversible heat and temperature?', 'entropy')),
        ('Exponentiate and normalize', 'The common exp(S₀/kB) cancels when all probabilities are normalized. The remaining weights are Boltzmann weights; Z is their sum.', 'Pi = exp(−βEi)/Z;  Z = Σi exp(−βEi);  β = 1/(kBT)'),
        ('Allow particle exchange', 'Define the reservoir chemical potential through (∂S/∂N)U,V = −μ/T. If the subsystem gains N particles the reservoir loses them; its entropy expansion therefore adds +μN/T.', 'wi,N ∝ exp[−β(Ei − μN)]'),
        ('Sum allowed state occupations', 'For one quantum state of energy E, set x = exp[−β(E − μ)]. Fermions permit n = 0 or 1, giving ⟨n⟩ = x/(1 + x). Bosons permit n = 0,1,2,…, so geometric sums Σxⁿ and Σnxⁿ give ⟨n⟩ = x/(1 − x). Photons have μ = 0.', 'ffermion = 1/[exp(β(E − μ)) + 1];  nboson = 1/[exp(β(E − μ)) − 1]'),
      ], 'If one classical state is kBT higher than another, its individual probability is smaller by a factor e, before counting any degeneracy.',
      'The derivation does not prove equal a priori weights from Newton’s laws. That equilibrium postulate and the thermodynamic identification of temperature are explicit foundations.')
