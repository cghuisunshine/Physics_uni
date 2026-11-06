"""Original teaching notes. Equations are Unicode text so they work offline and copy.

Each branch belongs to the particular step that needs the prerequisite, rather
than to an unrelated reading list. Edit here, then run build_derivations.py.
"""

TOPICS = []


def S(title, text, equation='', branch=None):
    return dict(title=title, text=text, equation=equation, branch=branch)


def T(chapter, slug, title, formula, meaning, symbols, assumptions, steps, example,
      caution, headings=()):
    TOPICS.append(dict(chapter=chapter, slug=slug, title=title, formula=formula,
                       meaning=meaning, symbols=symbols, assumptions=assumptions,
                       steps=steps, example=example, caution=caution,
                       headings=headings))


T(1, 'units-and-dimensions', 'Why unit conversions work',
  'quantity = numerical value × unit',
  'A measurement is a physical quantity, not just a number. Changing units changes the number while preserving the quantity. Dimensional analysis then checks whether a proposed equation could be meaningful.',
  'L, M, T denote dimensions of length, mass, and time; they are not particular units. A conversion factor is a ratio of two equal physical quantities.',
  'Units refer to the same kind of quantity. Dimensional consistency is necessary for an equation, but cannot determine dimensionless constants or prove a physical law.', [
    S('Write an equality between units', 'One kilometre is exactly one thousand metres. Divide this equality by either side: the resulting ratio is one. Multiplication by that ratio cannot change a physical quantity.', '1 km / (1000 m) = 1'),
    S('Cancel units as algebraic factors', 'Choose the orientation that cancels the original unit. Time is in the denominator of a speed, so the time conversion must be inverted relative to a distance conversion.', '72 km/h × (1000 m/km) × (1 h/3600 s) = 20 m/s'),
    S('Check dimensions on both sides', 'Acceleration has dimensions L/T². Multiplying it by a time squared produces a length, which can be added to another length. A velocity cannot be added directly to a position.', '[v₀t] = (L/T)T = L;  [at²] = (L/T²)T² = L'),
    S('See what dimensions cannot determine', 'Both at² and ½at² have the same dimension. The factor ½ comes from how velocity changes during the motion, not from unit analysis.', 'x − x₀ = v₀t + ½at²', ('Where does the factor ½ come from?', 'constant-acceleration')),
  ], 'A length of 2.5 cm is 0.025 m. An area of 2.5 cm² is 2.5 × 10⁻⁴ m², because the entire conversion factor must be squared.',
  'Do not convert square or cubic units using an unsquared or uncubed length factor.', ('Measurement in Physics', 'Changing Units'))

T(1, 'density', 'Density: a definition and its consequences', 'ρ = m/V;  dm = ρ dV',
  'Density describes how much mass occupies a given volume. The average-density formula is a definition. Integrating a specified local density to obtain total mass is a mathematical consequence of that definition.',
  'ρ: mass density (kg/m³); m: mass (kg); V: volume (m³). Local density may depend on position.',
  'Use m/V for average density; use a single constant ρ throughout an object only if it is uniform.', [
    S('Define the average', 'Divide the total mass by the total volume. This tells us the mass per unit volume, but says nothing by itself about whether different regions have different densities.', 'ρavg = m/V'),
    S('Resolve the object into small pieces', 'For a sufficiently small volume element around a point, define local density through the limiting ratio. The differential form tells us how to recover the mass of that element.', 'ρ = lim(ΔV → 0) Δm/ΔV;  dm = ρ dV'),
    S('Add all the elements', 'Integrating is the continuous version of summing the masses. If density is constant it can be taken outside the integral.', 'm = ∫volume ρ dV = ρV  (uniform density)', ('Why does adding small pieces give an integral?', 'integrals')),
    S('Check the scale', 'For uniform material, doubling the volume doubles the mass without changing the density. This makes density an intensive property.', 'ρ(2V) = (2m)/(2V) = ρ'),
  ], 'A uniform 0.002 m³ object of density 2700 kg/m³ has mass m = 2700 × 0.002 = 5.4 kg.',
  'Mass and weight differ: density uses mass, while weight also depends on the local gravitational field.', ('Density',))

T(2, 'constant-acceleration', 'Derive the constant-acceleration equations',
  'v = v₀ + at;  x = x₀ + v₀t + ½at²;  v² = v₀² + 2a(x − x₀)',
  'These three familiar equations follow by accumulating a constant acceleration and then accumulating the resulting velocity. The factor ½ records the triangular area under the changing part of the velocity graph.',
  'x₀, v₀: position and velocity at t = 0; a: signed acceleration; x, v: values at time t. Use one consistent axis.',
  'Acceleration is constant over the entire time interval. These are one-dimensional component equations.', [
    S('Accumulate acceleration', 'Acceleration is the rate of change of velocity. Integrate from initial time zero to time t. Since a is constant, its integral is at.', 'v − v₀ = ∫₀ᵗ a dt′ = at', ('Why is integration the reverse of taking a rate?', 'integrals')),
    S('Accumulate velocity', 'Substitute the velocity found in step 1 into dx/dt = v. The constant part produces v₀t; the linearly growing part produces half of at².', 'x − x₀ = ∫₀ᵗ (v₀ + at′) dt′ = v₀t + ½at²'),
    S('Eliminate time', 'Write the displacement as average velocity times time. Under constant acceleration the velocity graph is a straight line, so its average is the mean of its endpoints. Multiply by a and use at = v − v₀.', '2a(x − x₀) = (v + v₀)(v − v₀) = v² − v₀²'),
    S('Check the zero-acceleration limit', 'With a = 0, velocity stays constant and the displacement reduces to v₀t. This checks the structure of the equations; it does not extend them to variable acceleration.', 'a = 0 ⇒ v = v₀,  x − x₀ = v₀t'),
  ], 'Starting from rest with a = 2 m/s² for 3 s gives v = 6 m/s and displacement 9 m. The time-free equation checks this: 6² = 2 × 2 × 9.',
  'A slowing object does not automatically have negative acceleration: the sign depends on the chosen axis.', ('Constant Acceleration',))

T(2, 'rates-of-change', 'Velocity and acceleration from derivatives', 'vₓ = dx/dt;  aₓ = dvₓ/dt = d²x/dt²',
  'An average velocity measures change over a finite interval. Instantaneous velocity asks what that rate approaches as the interval shrinks. Acceleration repeats the same construction for velocity.',
  'x(t): position; Δt: a nonzero time interval; vₓ and aₓ: signed components along the x axis.',
  'The required derivatives exist at the time of interest. An idealized instantaneous impact may require impulse instead.', [
    S('Start with a measurable average', 'Record two positions and divide their difference by the elapsed time. Geometrically this is the slope of the secant connecting two points on x(t).', 'vavg,x = [x(t + Δt) − x(t)]/Δt'),
    S('Shrink the interval', 'The limit gives the slope of the tangent. This is the definition of instantaneous velocity, not an independent experimental law.', 'vₓ(t) = lim(Δt → 0) [x(t + Δt) − x(t)]/Δt'),
    S('Differentiate again', 'Apply the same rate construction to velocity. Positive acceleration means that the signed velocity is increasing, which can mean either speeding up or slowing down.', 'aₓ = lim(Δt → 0) [vₓ(t + Δt) − vₓ(t)]/Δt'),
    S('Reconstruct motion from a rate', 'Knowing acceleration does not determine a unique trajectory until an initial velocity and an initial position are supplied. Each integration introduces one such initial value.', 'vₓ(t) = vₓ(0) + ∫₀ᵗ aₓ(t′) dt′', ('How do initial values enter an integral?', 'integrals')),
  ], 'For x(t) = (3 m/s²)t² − (2 m/s)t, velocity is (6 m/s²)t − 2 m/s and acceleration is 6 m/s². At t = 0 the object moves in the negative x direction.',
  'Distance divided by time gives average speed. Displacement divided by time gives average velocity.', ('Average Velocity', 'Instantaneous Velocity', 'Acceleration'))

T(3, 'vector-components', 'Why vector components use sine and cosine', 'aₓ = a cos θ;  aᵧ = a sin θ;  a = √(aₓ² + aᵧ²)',
  'Resolving a vector means finding its projections on independent axes. The components are signed numbers; the vector itself is their sum multiplied by unit directions.',
  'a ≥ 0: magnitude; θ: angle measured from positive x toward positive y; î, ĵ: orthogonal unit vectors.',
  'The displayed trigonometric formulas use orthonormal Cartesian axes and the stated angle convention.', [
    S('Construct a right triangle', 'Draw the vector as the hypotenuse and drop a perpendicular to the x axis. The adjacent side divided by the hypotenuse is cos θ; the opposite side divided by it is sin θ.', 'cos θ = aₓ/a;  sin θ = aᵧ/a'),
    S('Retain the signs', 'The trigonometric definitions continue into all quadrants. For example, a vector pointing left and upward has a negative x component and a positive y component.', '𝐚 = aₓ î + aᵧ ĵ'),
    S('Rebuild the magnitude', 'Orthogonality makes the cross term vanish when the vector is dotted with itself. Pythagoras then gives the length.', '𝐚 · 𝐚 = aₓ² + aᵧ² = a²', ('Why does the dot product measure a projection?', 'vector-products')),
    S('Add vectors component by component', 'Collect the coefficients of the same independent unit directions. Magnitudes generally cannot be added directly because direction matters.', '(𝐚 + 𝐛)ₓ = aₓ + bₓ;  (𝐚 + 𝐛)ᵧ = aᵧ + bᵧ'),
  ], 'A 10 N vector at 150° has components −8.66 N and +5.00 N. Squaring and adding gives its original magnitude of 10 N.',
  'Use atan2(aᵧ, aₓ) to recover direction. A plain inverse tangent of aᵧ/aₓ loses the quadrant.', ('Components of a Vector', 'Unit Vectors'))

T(3, 'vector-products', 'Dot and cross products: what they measure', '𝐚 · 𝐛 = ab cos θ;  |𝐚 × 𝐛| = ab sin θ',
  'The dot product extracts the part of one vector along the other. The cross product measures the oriented area swept out by two vectors. Work uses the first; torque uses the second.',
  'a, b: nonnegative magnitudes; θ: angle between the vectors, from 0 to π. The cross-product direction follows the right-hand rule.',
  'The ordinary cross product here is a three-dimensional Euclidean construction with a right-handed coordinate basis.', [
    S('Project one vector onto the other', 'The component of 𝐚 along the direction of 𝐛 is a cos θ. Multiplying by b gives the dot product. Only the parallel part contributes.', '𝐚 · 𝐛 = (a cos θ)b = aₓbₓ + aᵧbᵧ + a_zb_z'),
    S('Interpret the sign', 'Parallel vectors give a positive dot product, perpendicular vectors give zero, and vectors pointing mostly opposite ways give a negative result.', 'θ = 90° ⇒ 𝐚 · 𝐛 = 0'),
    S('Build an area from base and height', 'A parallelogram with sides 𝐚 and 𝐛 has base a and perpendicular height b sin θ. The cross product has that magnitude and is perpendicular to the plane.', '|𝐚 × 𝐛| = a(b sin θ)'),
    S('Connect geometry to a force', 'For torque, only the force component perpendicular to the position vector changes angular momentum about the origin. A force directed straight toward the origin has zero lever arm.', '𝐫 × 𝐅 = 𝛕;  τ = rF sin θ', ('How does torque change angular momentum?', 'angular-momentum')),
  ], 'For 𝐚 = 2î and 𝐛 = 3ĵ, the dot product is zero and the cross product is 6k̂. Reversing the order of the cross product gives −6k̂.',
  'A dot product is a scalar. A cross product is a vector and changes sign when its operands are exchanged.', ('The Scalar Product', 'The Vector Product'))

T(4, 'projectile-motion', 'Derive the projectile trajectory', 'y = y₀ + (x − x₀)tan θ − g(x − x₀)²/(2v₀² cos² θ)',
  'Projectile motion combines constant horizontal velocity with constant vertical acceleration. The curved path comes from eliminating the shared time between those two motions.',
  'v₀: launch speed; θ: launch angle above horizontal; g > 0: gravitational acceleration magnitude. Upward is positive y.',
  'Negligible air resistance, a uniform downward gravitational field, and a launch with nonzero horizontal velocity.', [
    S('Resolve the launch velocity', 'Gravity acts vertically, so it does not change the horizontal component. Treat each component separately while using the same time.', 'v₀ₓ = v₀ cos θ;  v₀ᵧ = v₀ sin θ', ('Why these trigonometric factors?', 'vector-components')),
    S('Integrate each acceleration', 'Horizontal acceleration is zero and vertical acceleration is −g. Apply the one-dimensional constant-acceleration results to each direction.', 'x − x₀ = v₀ cos θ t;  y − y₀ = v₀ sin θ t − ½gt²'),
    S('Eliminate the shared time', 'Solve the horizontal equation for t and substitute it into the vertical one. The linear term gives the launch slope; the quadratic term bends the trajectory downward.', 't = (x − x₀)/(v₀ cos θ)'),
    S('Derive the equal-height range', 'Set y = y₀. Exclude the initial root t = 0 and solve for flight time. Substitution into the horizontal displacement yields the range.', 'tflight = 2v₀ sin θ/g;  R = v₀² sin(2θ)/g'),
  ], 'For v₀ = 20 m/s and θ = 30°, the equal-height flight time is about 2.04 s and the range is 35.3 m using g = 9.81 m/s².',
  'The range formula assumes equal launch and landing heights. At the highest point vᵧ = 0, but acceleration is still −g.', ('Projectile Motion',))

T(4, 'centripetal-acceleration', 'Why circular acceleration is v²/r', 'aᵣ = v²/r = ω²r',
  'Even at constant speed, velocity changes as its direction turns. The acceleration comes from this directional change and points toward the centre of the circle.',
  'r: fixed radius; v: speed; ω: angular speed in radians per second; Δθ: angle swept during Δt.',
  'The derivation uses uniform circular motion. For varying speed there is also tangential acceleration dv/dt.', [
    S('Compare two nearby velocity vectors', 'The vectors have the same length v. Rotate one through Δθ to obtain the other. The tip-to-tip difference has length 2v sin(Δθ/2).', '|Δ𝐯| = 2v sin(Δθ/2)'),
    S('Take the short-time limit', 'As the interval approaches zero, sin(Δθ/2)/(Δθ/2) approaches one. Thus the rate of velocity change becomes v times the angular turning rate.', 'a = lim |Δ𝐯|/Δt = v(dθ/dt) = vω'),
    S('Relate arc distance and angle', 'Radian measure is defined by arc length divided by radius. Differentiating s = rθ for fixed radius gives v = rω.', 'a = v(v/r) = v²/r'),
    S('Identify the inward direction', 'The velocity is tangent to the path; the difference between nearby tangents points toward the centre in the limit. Newton’s law therefore requires an inward net force.', 'Fnet,inward = mv²/r', ('Which real force supplies this acceleration?', 'newtons-second-law')),
  ], 'A body moving at 6 m/s around a 3 m radius circle has inward acceleration 12 m/s². Doubling the speed multiplies this acceleration by four.',
  'Centripetal force names the inward net force. It is supplied by actual interactions such as tension, gravity, or friction.', ('Uniform Circular Motion',))

T(5, 'newtons-second-law', 'What Newton’s second law assumes', 'Σ𝐅ext = d𝐩/dt = m𝐚  (constant mass)',
  'Newton’s second law is a foundational empirical law of classical mechanics. It connects interactions to changes in momentum; component equations and acceleration predictions follow from it.',
  '𝐩 = m𝐯: momentum; 𝐅ext: external force; m: constant mass; 𝐚: acceleration in an inertial frame.',
  'Classical speeds and an inertial frame. For variable-mass systems, identify momentum flowing across the system boundary before using a simple particle equation.', [
    S('Choose the system', 'Draw a boundary around the object. List forces exerted by things outside that boundary. Forces between parts inside the boundary are not additional external forces.'),
    S('Apply the law to momentum', 'The physical input is the relation between net external force and momentum change. For fixed mass the derivative of m𝐯 is m times the velocity derivative.', 'Σ𝐅ext = d(m𝐯)/dt = m d𝐯/dt'),
    S('Resolve onto independent axes', 'A vector equation holds along each Cartesian axis. Resolve oblique forces before summing their signed components.', 'ΣFₓ = maₓ;  ΣFᵧ = maᵧ', ('How do I resolve an angled force?', 'vector-components')),
    S('Use a constraint only when it applies', 'An object resting on a horizontal floor has zero vertical acceleration. With only its weight and the normal force vertically, their magnitudes must match. Other vertical forces or acceleration change that result.', 'N − mg = 0 ⇒ N = mg  (this setup only)'),
  ], 'A 4 kg box pulled rightward by 18 N while friction supplies 6 N leftward has aₓ = (18 − 6)/4 = 3 m/s².',
  'Action–reaction pairs act on different bodies. They do not cancel in the free-body diagram of one body.', ('Newton’s Second Law',))

T(5, 'inclined-plane', 'Derive the acceleration down an incline', 'a = g sin θ  (frictionless incline)',
  'On an incline, only the component of weight parallel to the surface accelerates the object along it. The perpendicular component is balanced by the surface when the object stays in contact.',
  'θ: incline angle above horizontal; m: mass; N: normal-force magnitude; positive direction: down the plane.',
  'A fixed, straight, frictionless incline; uniform gravity; no other applied forces; the object remains in contact.', [
    S('Rotate the axes', 'Choose one axis down the plane and another perpendicular outward. Rotating coordinates does not change the force; it makes the constraint easier to express.'),
    S('Project the weight', 'The geometry gives a component mg sin θ down the plane and mg cos θ into it. At θ = 0 the down-plane component must vanish, which checks the choice of sine.', 'W∥ = mg sin θ;  W⊥ = mg cos θ', ('Why does an angle produce these components?', 'vector-components')),
    S('Use the perpendicular constraint', 'The object neither leaves nor penetrates the plane, so perpendicular acceleration is zero. Newton’s law fixes the normal force.', 'N − mg cos θ = 0 ⇒ N = mg cos θ'),
    S('Apply Newton along the plane', 'Divide the parallel equation by mass. The cancellation explains why ideal blocks of different masses share the same acceleration.', 'ma = mg sin θ ⇒ a = g sin θ', ('How does friction modify this result?', 'friction')),
  ], 'At θ = 30°, a = g/2 ≈ 4.91 m/s². For a 2 kg object the normal force is about 17.0 N, less than its weight.',
  'N is mg cos θ here, not mg. A normal force is set by the perpendicular equation of motion.', ())

T(6, 'friction', 'Static and kinetic friction on an incline', 'fₛ ≤ μₛN;  fₖ = μₖN;  tan θcritical = μₛ',
  'The elementary friction relations are approximate empirical models. The onset-of-sliding angle and the sliding acceleration are consequences of combining those models with Newton’s law.',
  'μₛ, μₖ: dimensionless friction coefficients; N: normal-force magnitude; fₛ, fₖ: friction magnitudes.',
  'Dry surfaces described by the Coulomb friction model. For the incline result, only gravity and contact forces act; the slope is fixed.', [
    S('Find the force needed to remain at rest', 'Down the plane gravity supplies mg sin θ. Static friction adjusts upward to balance it as long as its maximum value is not exceeded.', 'fₛ,required = mg sin θ;  N = mg cos θ', ('Derive the weight components first', 'inclined-plane')),
    S('Apply the static limit', 'The inequality determines whether the required friction is available. Equality describes impending slip, not every static situation.', 'mg sin θ ≤ μₛmg cos θ'),
    S('Solve for the critical slope', 'For 0 ≤ θ < 90°, divide by mg cos θ. At the boundary the tangent of the angle equals the coefficient.', 'tan θ ≤ μₛ;  θcritical = arctan μₛ'),
    S('Switch models once it slides', 'For motion down the slope, kinetic friction acts up it. Substitute its magnitude in Newton’s equation. If the block instead moves up the slope, friction reverses direction.', 'ma = mg sin θ − μₖmg cos θ ⇒ a = g(sin θ − μₖ cos θ)'),
  ], 'With μₛ = 0.50, the limiting angle is 26.6°. A resting block on a 10° slope has friction mg sin 10°, less than μₛN.',
  'Static friction is not always μₛN. Its magnitude and direction respond to the tendency to slip.', ('Friction',))

T(6, 'terminal-speed', 'Derive terminal speed with quadratic drag', 'vterminal = √(2mg/(Cρair A))',
  'Terminal speed is the steady falling speed at which upward drag balances weight. It follows from a force balance once a drag model has been chosen.',
  'C: dimensionless drag coefficient; ρair: air density; A: projected area; v: downward speed; g: gravitational acceleration magnitude.',
  'One-dimensional downward motion, constant mass and air properties, approximately constant C, quadratic drag, and negligible buoyancy.', [
    S('State the drag model', 'For this regime the drag magnitude is proportional to v². It acts opposite the velocity. This is a model of the fluid interaction, not a consequence of Newton’s law alone.', 'D = ½Cρair Av²'),
    S('Write the equation of motion', 'Take downward as positive. Weight increases the downward velocity and drag reduces its rate of increase.', 'm dv/dt = mg − ½Cρair Av²', ('Why is the left side mass times acceleration?', 'newtons-second-law')),
    S('Set acceleration to zero', 'Terminal motion means constant velocity, so the two force magnitudes balance. Solve the resulting equation for the positive falling speed.', 'mg = ½Cρair Avterminal²'),
    S('Check stability and scaling', 'Below terminal speed, weight wins and speed increases. Above it, drag wins and speed decreases. The square root means quadrupling mass doubles the terminal speed if the other parameters stay fixed.'),
  ], 'For m = 80 kg, C = 1.0, ρair = 1.2 kg/m³ and A = 0.70 m², the model gives about 43 m/s. A changing body orientation changes A and C.',
  'Small particles in slow viscous flow can have drag proportional to v instead; their terminal-speed formula differs.', ('Drag Force and Terminal Speed',))

T(7, 'work-energy', 'Derive the work–kinetic energy theorem', 'Wnet = ΔK;  K = ½mv²',
  'Work accumulates the component of force along a displacement. Newton’s law turns that accumulated force into a change in a quantity proportional to speed squared: kinetic energy.',
  'Wnet: work by all forces; m: constant mass; 𝐯: velocity; d𝐫: displacement element; K: translational kinetic energy.',
  'Classical particle motion with constant mass in an inertial frame. For a rotating or deformable object, track the appropriate energy terms.', [
    S('Define work along a path', 'For a short displacement, only the force component along the motion transfers energy through work. Add those contributions along the trajectory.', 'dW = 𝐅 · d𝐫;  Wnet = ∫ Σ𝐅 · d𝐫', ('Why a dot product?', 'vector-products')),
    S('Substitute Newton’s law', 'Use d𝐫 = 𝐯 dt and Σ𝐅 = m d𝐯/dt. The time increments cancel inside the integral.', 'dWnet = m(d𝐯/dt) · 𝐯 dt = m𝐯 · d𝐯'),
    S('Recognize a derivative', 'The derivative of 𝐯 · 𝐯 is twice 𝐯 · d𝐯. Hence integrating the right-hand side gives one half of m times the change in speed squared.', 'Wnet = ½m(vf² − vi²)'),
    S('Name the energy', 'Define K = ½mv² so the result reads Wnet = Kf − Ki. Negative net work reduces speed; work by one individual force is only one contribution to the total.', 'ΔK = Wnet'),
  ], 'A net force of 10 N parallel to a 3 m displacement does 30 J of work. A 2 kg body starting from rest then has v = √30 ≈ 5.48 m/s.',
  'Zero net force means zero net work, but individual forces can still do nonzero works that cancel.', ('Kinetic Energy', 'The Work–Kinetic Energy Theorem', 'Work'))

T(7, 'spring-work', 'Why spring work contains ½kx²', 'Ws = ½kxi² − ½kxf²;  Us = ½kx²',
  'An ideal spring does not exert a constant force. Its force grows linearly with displacement from equilibrium, so the work is an area under a sloping line rather than force at the endpoint times distance.',
  'k > 0: spring constant (N/m); x: signed extension from equilibrium; Ws: work done by the spring.',
  'An ideal Hooke-law spring in its linear elastic range, with negligible internal losses.', [
    S('State the restoring-force model', 'The force points opposite the displacement. A positive extension gives a negative force along the x axis.', 'Fₛ = −kx'),
    S('Accumulate the changing force', 'Work by the spring is the integral of its force component with respect to displacement. Keep the initial and final limits to preserve the sign.', 'Ws = ∫ₓᵢˣᶠ (−kx) dx'),
    S('Integrate the linear function', 'The integral of x is x²/2. Equivalently, the force–position graph between zero and x is a triangle of base x and height kx.', 'Ws = −½k(xf² − xi²)', ('Why does integrating x produce x²/2?', 'integrals')),
    S('Define stored potential energy', 'For a conservative spring, energy stored increases by the negative of the work the spring does. Choose zero potential at the equilibrium length.', 'ΔUs = −Ws;  Us(x) = ½kx²', ('Why is conservative work minus a potential change?', 'potential-energy')),
  ], 'Compressing a 200 N/m spring by 0.10 m stores 1.0 J. A quasistatic external push does +1.0 J while the spring does −1.0 J.',
  'The final force magnitude times displacement is kx², twice the actual work required from zero extension.', ('Work Done by a Spring Force',))

T(8, 'potential-energy', 'Derive force from potential energy', 'ΔU = −∫ 𝐅conservative · d𝐫;  Fₓ = −dU/dx',
  'Potential energy packages path-independent work into a function of position. Its gradient tells us the direction and strength of the associated conservative force.',
  'U: potential energy; 𝐅conservative: conservative force; x: position coordinate. Only differences in U affect this force.',
  'The force is conservative in the region considered. In one dimension U is differentiable; in several dimensions use 𝐅 = −∇U.', [
    S('Require path-independent work', 'Between two fixed positions, a conservative force does the same work along every allowed path. This permits us to assign a potential difference to the two endpoints.'),
    S('Choose the sign of potential energy', 'If the force does positive work and kinetic energy increases, the corresponding potential decreases. Define the potential difference to enforce this energy exchange.', 'Uf − Ui = −Wconservative', ('How does work change kinetic energy?', 'work-energy')),
    S('Look at a very small displacement', 'For displacement dx in one dimension, the potential change is dU = −Fₓ dx. Divide by dx to obtain the local force.', 'Fₓ = −dU/dx'),
    S('Recover familiar examples', 'For U = mgy, differentiating gives Fᵧ = −mg. For U = ½kx² it gives Fₓ = −kx. A local minimum of U is a stable equilibrium if the surrounding force points back toward it.', 'dU/dx = 0 at equilibrium;  d²U/dx² > 0 implies a local stable minimum'),
  ], 'For U(x) = (2 J/m²)x², the force is Fₓ = −(4 N/m)x. At x = 0.50 m it is −2.0 N.',
  'Potential energy belongs to an interacting system. Adding a constant to U changes no predicted force.', ('Potential Energy', 'Finding Force from Potential Energy'))

T(8, 'mechanical-energy', 'When is mechanical energy conserved?', 'Δ(K + U) = Wnonconservative',
  'Mechanical energy is constant when all the work being tracked is represented by conservative potential energies. Other interactions transfer energy into or out of that mechanical account.',
  'K: kinetic energy; U: sum of included conservative potentials; Wnonconservative: work not already included through U.',
  'Apply the particle work–energy theorem consistently. For extended systems, include rotation, deformation, internal energy and boundary transfers as needed.', [
    S('Start with total work', 'The net work changes kinetic energy. Separate the force contributions into conservative forces and the remaining forces.', 'ΔK = Wconservative + Wnonconservative', ('Derive the work–energy theorem', 'work-energy')),
    S('Replace conservative work by a potential change', 'A conservative contribution is the negative change of its potential. This is a bookkeeping substitution, so do not count that same work again on the right.', 'ΔK = −ΔU + Wnonconservative'),
    S('Collect the mechanical terms', 'Move ΔU to the left. With no remaining work, the initial and final sums must be equal.', 'Wnonconservative = 0 ⇒ Ki + Ui = Kf + Uf'),
    S('Understand frictional energy transfer', 'For a block sliding over a fixed surface, kinetic friction does negative work on the block. In the larger block-plus-surface system that mechanical energy typically becomes thermal energy.', 'Wfriction = −fₖd  (constant opposing sliding friction)'),
  ], 'A body released from rest 2.0 m above a chosen zero level has bottom speed √(2gh) ≈ 6.26 m/s if losses and rotation are negligible.',
  'Failure of mechanical-energy conservation does not mean failure of total-energy conservation.', ('Conservation of Mechanical Energy',))

T(9, 'momentum-and-impulse', 'Derive impulse and momentum conservation', '𝐉 = ∫ Σ𝐅ext dt = Δ𝐩;  Σ𝐅ext = 0 ⇒ 𝐏constant',
  'Impulse measures an interaction accumulated over time. Momentum conservation follows when the net external impulse on the chosen system vanishes.',
  '𝐩: momentum of one particle; 𝐏: total system momentum; 𝐉: external impulse; all are vectors.',
  'Classical mechanics with a clearly chosen system. Internal Newtonian action–reaction forces cancel pairwise; include external impulses during the interval.', [
    S('Integrate the momentum law', 'Newton’s second law states that force is the rate of momentum change. Its time integral gives the momentum difference between endpoints.', '∫[ti,tf] 𝐅 dt = 𝐩f − 𝐩i', ('How does an integral accumulate a changing force?', 'integrals')),
    S('Add particles within a system', 'Forces between system particles appear as equal and opposite pairs, so they cancel when the momentum equations are added.', 'd𝐏/dt = Σ𝐅ext'),
    S('Set the external impulse to zero', 'With no net external impulse, total momentum before and after the event is equal. Individual particles can exchange large amounts of momentum.', 'Σmi𝐯i,before = Σmi𝐯i,after'),
    S('Distinguish collision types', 'All isolated collisions conserve total momentum. Kinetic energy is conserved only for elastic collisions; a perfectly inelastic collision has the objects stick together.', 'm₁u₁ + m₂u₂ = (m₁ + m₂)v  (sticking, one dimension)'),
  ], 'A 2 kg cart at 3 m/s sticks to a stationary 1 kg cart. Their shared velocity is 6/3 = 2 m/s. Kinetic energy falls from 9 J to 6 J.',
  'A zero net external force is sufficient, but zero total external impulse over the particular interval is the more general conservation condition.', ('Linear Momentum', 'Impulse', 'Conservation of Linear Momentum'))

T(9, 'center-of-mass', 'Why a system’s centre of mass obeys Newton’s law', '𝐑cm = (Σmi𝐫i)/M;  M𝐀cm = Σ𝐅ext',
  'The centre of mass is a mass-weighted average of position. Its special usefulness follows by differentiating that definition and adding the particle equations of motion.',
  'mi: particle masses; M = Σmi: total mass; 𝐑cm: centre-of-mass position; 𝐀cm: its acceleration.',
  'Fixed particle masses and total mass, an inertial frame, and cancelling internal action–reaction forces.', [
    S('Define the weighted position', 'Multiply each position by its mass, add the results, and divide by total mass. A heavier object pulls the weighted average closer to its own position.', 'M𝐑cm = Σmi𝐫i'),
    S('Differentiate once', 'Because the masses are constant, differentiating acts only on positions. The right side becomes the total momentum.', 'M𝐕cm = Σmi𝐯i = 𝐏'),
    S('Differentiate again', 'The momentum rate is the net external force. Internal forces rearrange the parts but do not alter the total momentum rate.', 'M𝐀cm = d𝐏/dt = Σ𝐅ext', ('Why do internal forces cancel?', 'momentum-and-impulse')),
    S('Extend to continuous matter', 'Replace the sum by an integral over small mass elements. With local density, dm = ρ dV determines the weighting.', '𝐑cm = (1/M) ∫ 𝐫 dm', ('How do density and mass elements connect?', 'density')),
  ], 'Two masses, 1 kg at x = 0 and 3 kg at x = 4 m, have xcm = (1×0 + 3×4)/4 = 3 m.',
  'The centre of mass need not lie inside material: for a uniform ring it lies at the empty centre.', ('Center of Mass',))

T(10, 'rotational-energy', 'Derive rotational kinetic energy and moment of inertia', 'Krot = ½Iω²;  I = ∫ r⊥² dm',
  'A rigid body is made of particles with different linear speeds. Adding their translational kinetic energies produces a rotational energy with a geometry-dependent coefficient: the moment of inertia.',
  'r⊥: perpendicular distance to the rotation axis; ω: angular speed; I: moment of inertia about that axis (kg·m²).',
  'A rigid body rotating about a specified fixed axis. The kinetic energy below concerns that rotation.', [
    S('Find each particle’s speed', 'A point at perpendicular radius r⊥ travels along a circle. Differentiating arc length gives its speed.', 'vi = ωr⊥,i'),
    S('Add the particle energies', 'Every particle contributes ½mivi². The angular speed is shared by a rigid body, so ω² can be factored out.', 'K = Σ½mi(ωr⊥,i)² = ½ω²Σmi r⊥,i²', ('Why is particle kinetic energy ½mv²?', 'work-energy')),
    S('Define the geometry factor', 'The remaining sum is I. For continuous matter, replace it by an integral. Moving the same mass farther from the axis increases I quadratically.', 'I = Σmi r⊥,i² = ∫ r⊥² dm'),
    S('Compute a uniform disk', 'Divide a thin disk into concentric rings. With surface density σ = M/(πR²), each ring has mass 2πσr dr. Integrate from zero to R.', 'I = 2πσ ∫₀ᴿ r³ dr = ½MR²'),
  ], 'A 2 kg uniform disk of radius 0.50 m has I = 0.25 kg·m². At ω = 4 rad/s its rotational kinetic energy is 2 J.',
  'Moment of inertia must always be paired with its axis. It is not a property of mass alone.', ('Rotational Inertia', 'Kinetic Energy of Rotation'))

T(10, 'parallel-axis', 'Derive the parallel-axis theorem', 'I = Icm + Md²',
  'Shifting a rotation axis away from the centre of mass increases the moment of inertia by total mass times the squared separation of the parallel axes.',
  'Icm: moment of inertia about an axis through the centre of mass; d: perpendicular separation of the parallel axes; M: total mass.',
  'The two axes are parallel, and the reference axis passes through the centre of mass.', [
    S('Place the centre of mass at the origin', 'Choose the original axis along z and shift the new parallel axis by distance d in the x direction. A mass element has coordinates x, y relative to the original axis.', 'rnew² = (x − d)² + y²'),
    S('Expand the new squared radius', 'Moment of inertia uses perpendicular squared distance, so substitute the expansion under the mass integral.', 'I = ∫ (x² + y² − 2dx + d²) dm', ('Why integrate squared distance over mass?', 'rotational-energy')),
    S('Use the defining centre-of-mass condition', 'At a centre-of-mass origin, ∫x dm = 0. Thus the term linear in d disappears; this is exactly why the reference axis must be central.', '∫ x dm = Mxcm = 0'),
    S('Identify the remaining pieces', 'The first two squared coordinates give Icm. The constant d² factors out of the last integral and ∫dm = M.', 'I = Icm + d²∫dm = Icm + Md²'),
  ], 'A uniform rod of length L has central transverse inertia ML²/12. A parallel axis at one end gives Iend = ML²/12 + M(L/2)² = ML²/3.',
  'Do not add Md² to an arbitrary noncentral moment of inertia. First refer both axes to the relevant central parallel axis.', ('Parallel-Axis Theorem',))

T(11, 'angular-momentum', 'Derive torque as the rate of angular momentum', '𝐋 = 𝐫 × 𝐩;  𝛕ext = d𝐋/dt',
  'Angular momentum measures motion about a chosen origin. Differentiating its definition shows that torque is what changes it, just as force changes linear momentum.',
  '𝐫: position from a fixed origin; 𝐩 = m𝐯: particle momentum; 𝐋: angular momentum; 𝛕: torque about that same origin.',
  'A fixed origin in an inertial frame and classical particles. For a system, internal torques must cancel for only external torques to remain.', [
    S('Define angular momentum', 'The cross product selects the part of momentum perpendicular to the position vector. Radial motion has zero angular momentum about that origin.', '𝐋 = 𝐫 × m𝐯', ('Why does the cross product measure turning?', 'vector-products')),
    S('Apply the product rule', 'Differentiate both factors. The first term contains velocity crossed with itself, so it vanishes.', 'd𝐋/dt = 𝐯 × m𝐯 + 𝐫 × d𝐩/dt = 𝐫 × 𝐅'),
    S('Recognize torque', 'Define torque as 𝐫 × 𝐅. Its direction gives the axis of the induced change in angular momentum.', 'd𝐋/dt = 𝛕'),
    S('Specialize to a rigid fixed-axis rotation', 'For a body rotating about a fixed principal axis, the component along the axis is Laxis = Iω. If I is constant, differentiating gives the scalar rotational law. Vanishing external torque conserves L even if I changes.', 'τaxis = Iα;  Iᵢωᵢ = Ifωf  (zero external torque about that axis)'),
  ], 'A skater reducing axial inertia from 4 to 2 kg·m² doubles angular speed if external torque about that axis is negligible. Their rotational kinetic energy increases through muscular work.',
  'Torque and angular momentum depend on the chosen origin. In general 𝐋 need not be parallel to angular velocity.', ('Angular Momentum', 'Newton’s Second Law in Angular Form', 'Torque'))

T(11, 'rolling', 'Derive the speed of an object rolling downhill', 'v² = 2gh/(1 + Icm/(mR²))',
  'A rolling object uses its lost gravitational potential energy for both translation and rotation. The no-slip condition connects these two kinds of motion.',
  'v: centre-of-mass speed; R: rolling radius; Icm: axial inertia through the centre of mass; h: vertical descent.',
  'Rigid body starts at rest, rolls without slipping on a fixed surface, and has negligible rolling resistance and other energy loss.', [
    S('Apply the no-slip condition', 'The point instantaneously touching the fixed surface has zero velocity. The translational and rotational contributions there cancel.', 'v = ωR'),
    S('Separate translation and rotation', 'Relative to the centre of mass, internal rotational motion adds ½Icmω² to the kinetic energy of the centre’s motion.', 'K = ½mv² + ½Icmω²', ('Where does rotational kinetic energy come from?', 'rotational-energy')),
    S('Conserve mechanical energy', 'The decrease mgh supplies both terms. Static friction can supply the needed torque while doing no work at a no-slip contact on an ideal fixed surface.', 'mgh = ½mv² + ½Icm(v/R)²'),
    S('Solve for the speed', 'Factor v² and divide. A larger dimensionless inertia Icm/(mR²) gives a smaller final translational speed.', 'v² = 2gh/[1 + Icm/(mR²)]'),
  ], 'For a uniform solid cylinder Icm = ½mR², so v² = 4gh/3. For a thin hoop Icm = mR², so v² = gh. The cylinder reaches the larger speed.',
  'If the surface lacks sufficient static friction, slipping occurs and v = ωR cannot be imposed.', ('Rolling Bodies',))

T(12, 'static-equilibrium', 'Why equilibrium needs both force and torque balance', 'Σ𝐅ext = 0;  Σ𝛕ext = 0',
  'A body can have no translational acceleration yet still begin rotating. Static equilibrium therefore requires two independent balances, together with the initial condition that the body is at rest.',
  '𝐅ext: external forces; 𝛕ext: external torques about a chosen fixed origin; r⊥: perpendicular lever arm.',
  'A rigid body initially at rest in an inertial frame. Balancing forces and torques is necessary for equilibrium, but does not by itself establish stability.', [
    S('Stop the centre of mass from accelerating', 'Apply Newton’s law to the entire object. The centre of mass has zero acceleration only when the vector sum of external forces vanishes.', 'M𝐀cm = Σ𝐅ext = 0'),
    S('Stop angular momentum from changing', 'Two equal opposite forces at different points can form a couple: zero net force but nonzero net torque. Requiring torque balance excludes this rotational acceleration.', 'd𝐋/dt = Σ𝛕ext = 0', ('Derive the torque law', 'angular-momentum')),
    S('Choose a convenient pivot', 'Torque from a force is its magnitude times its perpendicular lever arm, with a sign for rotational sense. A support force acting at the chosen pivot contributes no torque about it.', 'τ = ±Fr⊥'),
    S('Check that the result is origin-independent', 'Shifting the torque origin by vector 𝐚 changes total torque by −𝐚 × Σ𝐅ext. Once force balance holds, a zero torque sum at one origin is zero at every origin.', 'Σ𝛕new = Σ𝛕old − 𝐚 × Σ𝐅ext'),
  ], 'A uniform 4 m beam weighs 200 N and is supported at its ends. Taking torque about the left end gives Nright × 4 − 200 × 2 = 0, so each support carries 100 N.',
  'An object moving at constant velocity can satisfy both balances without being in static equilibrium in your frame.', ('Static Equilibrium',))

T(12, 'elasticity', 'Derive the elastic extension of a rod', 'ΔL = FL/(AY)',
  'Young’s modulus expresses a material’s linear relation between tensile stress and strain. Solving that constitutive relation determines how a uniform rod stretches.',
  'F: axial tensile force; A: cross-sectional area; L: original length; ΔL: extension; Y: Young’s modulus (Pa).',
  'Uniform rod under axial load, approximately uniform stress, small strain, and elastic behaviour within the linear regime.', [
    S('Describe force per area', 'Two rods of different thickness do not respond identically to the same force. Stress measures the load relative to the cross section.', 'stress = F/A'),
    S('Describe fractional extension', 'A longer rod stretches more under the same material stress. Strain removes the original length from the comparison and is dimensionless.', 'strain = ΔL/L'),
    S('State the material law', 'Experiments in the linear elastic regime give stress proportional to strain. Their ratio defines Young’s modulus; it is not obtained from force balance alone.', 'F/A = Y(ΔL/L)'),
    S('Rearrange and connect to a spring', 'Solve for extension. The same rod acts like a spring with stiffness YA/L when its length and cross section can be treated as constant.', 'F = (YA/L)ΔL;  keffective = YA/L', ('What energy does this effective spring store?', 'spring-work')),
  ], 'A 2 m rod with A = 10⁻⁴ m² and Y = 2 × 10¹¹ Pa stretches 10⁻⁴ m under a 1000 N axial load.',
  'Young’s modulus describes a material; spring constant also depends on geometry. Beyond the elastic range this formula can fail.', ('Elasticity',))

T(13, 'orbital-speed', 'Derive circular-orbit speed and Kepler’s third law', 'v = √(GM/r);  T² = 4π²r³/(GM)',
  'A circular orbit is continuous free fall: gravity supplies exactly the inward acceleration required by the curved path. Combining those relations fixes both speed and period.',
  'M: central mass; m: orbiting mass; r: centre-to-centre radius; G: gravitational constant; T: orbital period.',
  'Newtonian gravity, an isolated approximately spherical central body, a circular orbit outside that body, and m much smaller than M.', [
    S('State the gravitational force', 'For the spherical central body, the exterior field is the same as that of a point mass at its centre. Gravity is the inward force on the satellite.', 'Fg = GMm/r²'),
    S('Impose circular acceleration', 'Set the force equal to mass times the required inward acceleration. The satellite mass cancels.', 'GMm/r² = mv²/r', ('Why is circular acceleration v²/r?', 'centripetal-acceleration')),
    S('Solve for speed and period', 'Solve the force balance for v². Divide the circumference by speed to obtain one revolution’s duration.', 'v² = GM/r;  T = 2πr/v'),
    S('Eliminate speed', 'Square the period and substitute v². This gives the circular-orbit form of Kepler’s third law. For bound ellipses, r is replaced by semimajor axis a.', 'T² = 4π²r²/(GM/r) = 4π²r³/(GM)'),
  ], 'Using Earth’s GM ≈ 3.986 × 10¹⁴ m³/s² and r = 7.0 × 10⁶ m gives v ≈ 7.55 km/s and T ≈ 97 min.',
  'Orbital radius is measured from the centre, not from the surface. For comparable masses, the relative-orbit period uses G(M + m).', ('Satellites: Orbits and Energy', 'Kepler’s Laws'))

T(13, 'escape-speed', 'Derive gravitational potential and escape speed', 'U(r) = −GMm/r;  vescape = √(2GM/r)',
  'Gravity weakens with distance, so escaping requires a finite amount of work. Integrating its inverse-square force gives the required energy and the minimum ideal escape speed.',
  'r: distance from the central mass; U: potential energy with zero at infinity; M: central mass; m: escaping mass.',
  'Newtonian isolated spherical central body, exterior motion, negligible air resistance, and no additional propulsion after launch.', [
    S('Choose the potential reference', 'Set U(∞) = 0. In the outward radial direction, gravity has component Fr = −GMm/r².', 'U(r) − U(∞) = −∫∞ʳ Fr dr′'),
    S('Integrate the inverse square', 'The antiderivative of 1/r² is −1/r. Keeping both the force sign and the potential definition gives a negative bound-state potential.', 'U(r) = −GMm/r', ('Why is potential change minus force integrated?', 'potential-energy')),
    S('Describe marginal escape', 'The minimum unbound trajectory reaches arbitrarily large distance with speed approaching zero. Its total mechanical energy is therefore zero.', '½mvescape² − GMm/r = 0'),
    S('Solve and compare with circular motion', 'Cancel m and solve the energy equation. At the same radius the escape speed is √2 times the circular-orbit speed.', 'vescape² = 2GM/r = 2vcircular²'),
  ], 'At Earth’s surface, r ≈ 6.37 × 10⁶ m gives an ideal escape speed about 11.2 km/s. This neglects rotation and atmospheric drag.',
  'The near-surface expression mgh assumes almost constant g. It cannot be extrapolated all the way to infinity.', ('Gravitational Potential Energy', 'Escape Speed'))

T(14, 'hydrostatic-pressure', 'Derive pressure with depth and buoyancy', 'p = p₀ + ρgh;  Fb = ρfluid gVdisplaced',
  'Pressure increases downward because lower layers support the weight above them. The resulting pressure difference across an immersed object produces buoyancy.',
  'ρ: fluid density; h: depth below a reference surface; p₀: surface pressure; Fb: upward buoyant-force magnitude.',
  'Fluid at rest, uniform density and gravitational field. The simple buoyancy expression uses the displaced volume in that uniform fluid.', [
    S('Isolate a thin horizontal slab', 'For slab area A and thickness dz, choose upward as positive. Pressure on the bottom pushes up, pressure on the top pushes down, and the slab has weight ρgA dz.', 'p(z)A − p(z + dz)A − ρgA dz = 0'),
    S('Take the differential limit', 'Divide by A dz and let thickness approach zero. The pressure gradient is negative upward.', 'dp/dz = −ρg'),
    S('Integrate to a depth h', 'For constant density, moving downward by h increases the pressure by ρgh.', 'pbelow − p₀ = ρgh', ('How does a gradient accumulate over distance?', 'integrals')),
    S('Replace an object by the fluid it displaced', 'The surrounding pressure forces would support that volume of fluid if it were present at rest. Therefore their resultant on an object of the same boundary equals the weight of displaced fluid.', 'Fb = mdisplacedg = ρfluidVdisplacedg'),
  ], 'At 2.0 m depth in water, gauge pressure is about 19.6 kPa. An immersed 0.003 m³ volume displaces water of weight about 29.4 N.',
  'Buoyant force depends on displaced fluid density, not object density. Absolute pressure includes p₀; gauge pressure subtracts it.', ('Fluids at Rest', 'Archimedes’ Principle'))

T(14, 'bernoulli', 'Derive continuity and Bernoulli’s equation', 'Av = constant;  p + ½ρv² + ρgy = constant',
  'Continuity expresses conservation of mass. Bernoulli’s equation expresses mechanical-energy conservation for a small portion of ideal flowing fluid along a streamline.',
  'A: flow cross section; v: local speed; p: pressure; y: elevation; ρ: fluid density.',
  'Steady, incompressible flow for Av = constant. Bernoulli additionally neglects viscosity and pumps or turbines between the two points; compare points along one streamline.', [
    S('Conserve transported mass', 'In time dt a stream tube passes volume Av dt through a section. In steady flow the mass entering equals the mass leaving.', 'ρ₁A₁v₁ = ρ₂A₂v₂;  A₁v₁ = A₂v₂  (constant ρ)'),
    S('Follow a small volume', 'Pressure upstream does positive work p₁dV while the downstream pressure opposes the motion and does −p₂dV. The net pressure work changes kinetic and gravitational energy.'),
    S('Apply the work–energy balance', 'The same mass dm = ρdV moves between the locations. Write its energy changes and divide by dV.', '(p₁ − p₂)dV = ½ρdV(v₂² − v₁²) + ρdVg(y₂ − y₁)', ('Why does work become a change of kinetic energy?', 'work-energy')),
    S('Rearrange the balance', 'Collect the quantities belonging to each endpoint. All terms have units of pressure, equivalently energy per volume.', 'p₁ + ½ρv₁² + ρgy₁ = p₂ + ½ρv₂² + ρgy₂'),
  ], 'In a horizontal ideal pipe, if water speeds up from 2 to 4 m/s, its pressure falls by ½(1000)(16 − 4) = 6000 Pa.',
  'A faster speed does not imply lower pressure in arbitrary flows. Apply the stated energy assumptions and compare appropriate points.', ('The Equation of Continuity', 'Bernoulli’s Equation'))

T(15, 'simple-harmonic-motion', 'Derive simple harmonic motion from a spring', 'x = A cos(ωt + φ);  ω = √(k/m);  T = 2π√(m/k)',
  'A restoring force proportional to displacement creates acceleration proportional to minus displacement. Sinusoids are the functions whose second derivatives have exactly that form.',
  'A: amplitude; φ: phase set by initial conditions; k: spring constant; m: oscillating mass; ω: angular frequency.',
  'Ideal linear spring, constant mass, no damping or driving. Measure x from the equilibrium position.', [
    S('Combine the force model with Newton’s law', 'Hooke’s law supplies the restoring force and Newton’s law supplies its effect on motion.', 'm d²x/dt² = −kx'),
    S('Identify the differential equation', 'Divide by m and define ω² = k/m. The minus sign means acceleration points back toward equilibrium.', 'd²x/dt² = −ω²x'),
    S('Verify the sinusoidal solution', 'Differentiate A cos(ωt + φ) twice. Its second derivative is −ω² times itself, so it satisfies the equation. A and φ remain to be set by initial position and velocity.', 'v = −Aω sin(ωt + φ);  a = −Aω² cos(ωt + φ)', ('What does a derivative mean physically?', 'rates-of-change')),
    S('Find the period', 'The phase advances by 2π during a complete cycle. Thus ωT = 2π, giving the period independently of amplitude in this linear model.', 'T = 2π/ω = 2π√(m/k)'),
  ], 'For m = 0.50 kg and k = 200 N/m, ω = 20 rad/s and T ≈ 0.314 s. At amplitude 0.05 m the maximum speed is Aω = 1 m/s.',
  'Zero displacement means maximum speed, not zero acceleration and speed together. At a turning point speed is zero but acceleration is largest.', ('Simple Harmonic Motion',))

T(15, 'pendulum', 'Derive the small-angle pendulum period', 'T ≈ 2π√(ℓ/g)',
  'A pendulum is approximately harmonic only at small angles. The approximation replaces sin θ by θ, turning its exact nonlinear equation into the spring-like harmonic equation.',
  'ℓ: distance from pivot to point mass; θ: angle from the downward vertical in radians; g: gravitational acceleration magnitude.',
  'Point bob, massless inextensible string or rod, fixed pivot, negligible friction and air drag. The period formula requires small angular amplitude.', [
    S('Find the restoring torque', 'Tension passes through the pivot and contributes no torque about it. Weight has perpendicular lever arm ℓ sin θ and restores the bob toward the bottom.', 'τ = −mgℓ sin θ'),
    S('Use rotational dynamics', 'The bob’s moment of inertia is mℓ². Substitute in τ = Iα and cancel the mass.', 'mℓ² d²θ/dt² = −mgℓ sin θ'),
    S('Make the small-angle approximation', 'For |θ| much smaller than one radian, sin θ ≈ θ. This is the sole step that makes the equation harmonic and its period approximately amplitude-independent.', 'd²θ/dt² ≈ −(g/ℓ)θ', ('Why does this equation give a sinusoid?', 'simple-harmonic-motion')),
    S('Read off the angular frequency', 'Compare the coefficient with −ω²θ. The oscillation period is then 2π/ω.', 'ω ≈ √(g/ℓ);  T ≈ 2π√(ℓ/g)'),
  ], 'A 1.0 m pendulum has a small-angle period about 2.01 s at g = 9.81 m/s². At a 5° amplitude, θmax ≈ 0.087 rad, so the approximation is good.',
  'Use radians in sin θ ≈ θ. Large-amplitude pendulums have longer periods than this approximation predicts.', ('Pendulums',))

T(16, 'wave-speed', 'Derive wave speed on a stretched string', 'v = √(𝒯/μ);  ∂²y/∂t² = (𝒯/μ)∂²y/∂x²',
  'String tension supplies a transverse force when a short segment is curved. Newton’s law links that curvature to transverse acceleration, producing the wave equation.',
  '𝒯: approximately constant string tension (N); μ: mass per unit length (kg/m); y(x,t): small transverse displacement.',
  'Uniform flexible string, small slopes, approximately constant tension, negligible damping and bending stiffness.', [
    S('Isolate a short segment', 'A segment of length dx has mass μdx. Equal tensions at its ends point along slightly different tangents, giving a small net transverse force.'),
    S('Express force through slope change', 'For small angles, the transverse tension component is approximately 𝒯 ∂y/∂x. The difference of its values at the two ends is curvature times 𝒯dx.', 'Fᵧ ≈ 𝒯(∂²y/∂x²)dx'),
    S('Apply Newton’s second law', 'Equate transverse force to segment mass times transverse acceleration. Cancel dx.', 'μdx(∂²y/∂t²) = 𝒯dx(∂²y/∂x²)'),
    S('Identify the propagation speed', 'For a travelling shape y = f(x − vt), two time derivatives give v²f″ and two space derivatives give f″. Substituting leaves v² = 𝒯/μ.', 'v²f″ = (𝒯/μ)f″ ⇒ v = √(𝒯/μ)', ('How do position and time derivatives differ?', 'rates-of-change')),
  ], 'A string at 100 N tension with μ = 0.010 kg/m carries small transverse waves at 100 m/s. Increasing tension by four doubles the speed.',
  'The string material moves mainly transversely; it does not travel down the string at the wave speed.', ('Speed of a Traveling Wave',))

T(16, 'standing-waves', 'Derive the allowed frequencies of a fixed string', 'λn = 2L/n;  fn = nv/(2L),  n = 1, 2, 3, …',
  'Waves reflected from the ends can form a standing pattern. Fixed ends require nodes at both boundaries, allowing only whole numbers of half-wavelengths inside the string length.',
  'L: vibrating string length; v: wave propagation speed; n: positive integer mode number; fn: frequency of mode n.',
  'Uniform string, fixed endpoints, linear waves, and negligible damping for the ideal mode frequencies.', [
    S('Superpose counterpropagating waves', 'Two equal waves travelling in opposite directions combine into a product of a spatial factor and a time factor. Points where the spatial factor is zero remain at rest.', 'y(x,t) = 2A sin(kx) cos(ωt)'),
    S('Impose the first boundary', 'Choosing sin(kx) makes x = 0 a node automatically. A fixed right end requires sin(kL) = 0 as well.', 'sin(kL) = 0 ⇒ kL = nπ'),
    S('Relate wavenumber and wavelength', 'A phase change of 2π corresponds to one wavelength. Substitute k = 2π/λ into the boundary condition.', '2πL/λn = nπ ⇒ λn = 2L/n'),
    S('Convert wavelength to frequency', 'A crest travels one wavelength per cycle, so v = fλ. The wave speed is set by the string tension and linear density.', 'fn = v/λn = nv/(2L)', ('Where does the string’s wave speed come from?', 'wave-speed')),
  ], 'For L = 0.50 m and v = 100 m/s, the fundamental is 100 Hz, followed by 200 Hz and 300 Hz.',
  'n = 0 gives no oscillating displacement for these fixed-end modes. Other boundary conditions produce different frequency sequences.', ('Standing Waves', 'Resonance'))

T(17, 'sound-speed', 'Why sound speed is √(B/ρ)', 'v = √(B/ρ)',
  'A sound wave alternately compresses and expands a medium. Its elastic resistance to compression drives the motion, while mass density resists acceleration.',
  'B: appropriate bulk modulus (Pa); ρ: equilibrium mass density; ξ(x,t): small longitudinal displacement.',
  'Small-amplitude plane longitudinal waves in a homogeneous fluid. Use the modulus appropriate to the thermal process; ordinary gas sound is approximately adiabatic.', [
    S('Relate compression to pressure', 'If displacement varies along x, neighbouring fluid elements change separation. To first order the fractional volume change is ∂ξ/∂x. The bulk modulus relates this to pressure perturbation.', 'δp = −B ∂ξ/∂x'),
    S('Find the force on a slab', 'The pressure difference across area A and thickness dx produces a net force −A(∂δp/∂x)dx. Its mass is ρA dx.'),
    S('Use Newton’s equation', 'Divide force equals mass times acceleration by A dx, then substitute the pressure–compression relation.', 'ρ ∂²ξ/∂t² = −∂δp/∂x = B ∂²ξ/∂x²'),
    S('Recognize a wave equation', 'The ratio multiplying the spatial second derivative is the square of the propagation speed. For an ideal gas, the adiabatic bulk modulus is γp.', 'v² = B/ρ;  videal gas = √(γp/ρ)', ('Why is an ideal-gas adiabatic process different?', 'adiabatic-gas')),
  ], 'For air with B ≈ 1.42 × 10⁵ Pa and ρ ≈ 1.20 kg/m³, this gives about 344 m/s.',
  'Using the isothermal gas modulus p instead of the adiabatic γp gives an incorrect value for ordinary sound propagation.', ('Sound Waves',))

T(17, 'doppler', 'Derive the sound Doppler formula', 'fobserved = fsource (v + uobserver)/(v − usource)',
  'Source motion changes crest spacing in the medium. Observer motion changes how quickly those crests are encountered. These are separate effects for sound because the medium defines a rest frame.',
  'v: sound speed relative to the medium; usource: source speed toward observer; uobserver: observer speed toward source; fsource: emitted frequency.',
  'Collinear motion, stationary homogeneous medium, constant subsonic source speed, and positive closing-speed conventions as defined here.', [
    S('Track two successive emissions', 'The source emits crests a period Ts = 1/fs apart. In that time the first crest moves vTs while the source moves usourceTs toward it.', 'λahead = (v − usource)Ts'),
    S('Convert spacing to frequency at rest', 'A stationary observer meets crests at rate v/λahead. The shortened spacing makes an approaching source sound higher.', 'frest observer = vfs/(v − usource)'),
    S('Let the observer approach', 'The crest–observer closing speed is v + uobserver. Divide this encounter speed by the spacing to obtain the arrival rate.', 'fobserved = (v + uobserver)/λahead'),
    S('Substitute and check the limit', 'Replacing λahead gives the stated formula. With both velocities zero the observed and emitted frequencies agree. For receding motion use a negative value for the corresponding defined closing speed.', 'fobserved = fs(v + uobserver)/(v − usource)'),
  ], 'With sound speed 340 m/s, an approaching 20 m/s source emitting 500 Hz is heard by a stationary listener at 500 × 340/320 = 531 Hz.',
  'This is the sound formula in a medium, not the relativistic light Doppler formula. At sonic source speeds a shock-wave treatment is needed.', ('The Doppler Effect',))

T(18, 'first-law', 'The first law and work by an expanding gas', 'ΔEint = Q − Wby;  Wby = ∫ pext dV',
  'The first law is energy conservation for a thermodynamic system. Heat and work describe transfers across its boundary; internal energy describes a property of the state.',
  'Q: heat transferred into the system; Wby: work done by it on the surroundings; Eint: internal energy; pext: boundary opposing pressure.',
  'A closed system with negligible changes in bulk kinetic and gravitational potential energy. For the simple integral use pressure–volume boundary work; additional kinds of work require additional terms.', [
    S('Choose signs before calculating', 'Energy entering as heat raises the system energy. Work delivered outward removes energy. This fixes the sign convention, rather than being a separate formula to memorize.', 'ΔEint = Q − Wby'),
    S('Find a piston’s small work', 'An outward displacement dx moves a piston of area A through volume change dV = A dx. Work delivered against the exterior pressure is force times displacement.', 'δWby = (pextA)dx = pext dV'),
    S('Accumulate along the actual path', 'Integrate boundary pressure over the volume change. In a quasistatic mechanically balanced process pext is approximately the gas pressure. For free expansion pext = 0 even though the gas expands.', 'Wby = ∫ᵥᵢᵛᶠ pext dV', ('Why does work depend on the path?', 'integrals')),
    S('Distinguish a state change from transfers', 'Internal-energy change depends only on endpoints. Heat and work generally depend on the process, so their infinitesimals are written δQ and δW rather than exact differentials.', 'dEint = δQ − δWby'),
    S('Derive the special-process limits', 'At constant volume the boundary work vanishes, so ΔU = Q. In a complete cycle ΔU = 0, so Q = Wby. For an insulated free expansion, Q = 0 and external pressure is zero, hence Wby = 0 and ΔU = 0. For a fixed amount of ideal gas with positive heat capacity, ΔU = 0 implies unchanged temperature, so its endpoint pV product is unchanged.', 'constant V: ΔU = Q;  cycle: Q = Wby;  insulated free expansion: ΔU = 0;  ideal gas ⇒ Tf = Ti and pfVf = piVi', ('Why does ideal-gas internal energy depend only on temperature?', 'heat-capacities')),
  ], 'If a gas absorbs 500 J of heat and does 200 J of work on a piston, its internal energy increases by 300 J.',
  'An isothermal ideal gas has ΔEint = 0 but can have nonzero heat and work. Adiabatic means Q = 0, not constant temperature.', ('The First Law of Thermodynamics', 'Heat and Work'))

T(18, 'isothermal-work', 'Derive the logarithm in isothermal gas work', 'Wby = nRT ln(Vf/Vi)  (reversible isothermal ideal gas)',
  'An ideal gas at constant temperature has pressure inversely proportional to volume. Integrating that decreasing pressure gives a logarithm.',
  'n: fixed amount in moles; R: gas constant; T: constant absolute temperature; Vi, Vf: initial and final volumes.',
  'Ideal gas, fixed amount, reversible or quasistatic mechanically balanced expansion or compression, and constant temperature maintained by heat exchange.', [
    S('Use the equation of state', 'During an isothermal path nRT is constant, but pressure changes as volume changes. Thus pressure cannot be pulled out of the work integral.', 'p(V) = nRT/V', ('Why does the ideal gas obey pV = nRT?', 'ideal-gas')),
    S('Use the reversible work expression', 'For mechanical equilibrium at each step, the boundary pressure equals the gas pressure in the reversible limit.', 'Wby = ∫ᵥᵢᵛᶠ p(V)dV = nRT ∫ᵥᵢᵛᶠ dV/V'),
    S('Integrate reciprocal volume', 'The derivative of ln V is 1/V. Evaluating the antiderivative at two endpoints produces a logarithm of their ratio, whose argument is dimensionless.', 'Wby = nRT(ln Vf − ln Vi) = nRT ln(Vf/Vi)'),
    S('Use the first law for the heat', 'Ideal-gas internal energy depends only on temperature. Here its change is zero, so the absorbed heat equals the work done by the gas.', 'ΔEint = 0 ⇒ Q = Wby', ('Why does the first law have this sign?', 'first-law')),
  ], 'One mole of ideal gas at 300 K expanding reversibly to twice its volume does 8.314 × 300 × ln 2 ≈ 1.73 kJ of work.',
  'The same endpoints reached by free expansion give Wby = 0, not this logarithmic work. Reversibility and path matter.', ())

T(19, 'ideal-gas', 'Derive pV = nRT from molecular collisions', 'pV = ⅓Nm⟨v²⟩ = NkBT = nRT',
  'Pressure arises from momentum delivered to walls. The collision calculation produces a mechanical relation; an equilibrium energy–temperature relation then introduces temperature.',
  'N: molecule count; m: one molecule’s mass; n: moles; kB: Boltzmann constant; R = NAkB; ⟨v²⟩: mean square speed.',
  'Classical dilute gas of effectively point particles, negligible intermolecular potential energy, elastic wall collisions, isotropic thermal equilibrium, and nonrelativistic motion.', [
    S('Track repeated impacts on one wall', 'In a cube of side L, one molecule reverses its x momentum on reflection. The wall receives 2m|vₓ| per impact; the return time is 2L/|vₓ|.', 'Fone,average = (2m|vₓ|)/(2L/|vₓ|) = mvₓ²/L'),
    S('Add molecules and divide by area', 'The wall area is L² and the volume is L³. Summing the momentum flux gives pressure in terms of one velocity component.', 'pV = mΣvₓ,i² = Nm⟨vₓ²⟩'),
    S('Use isotropy', 'No direction is preferred in equilibrium. Equal mean-square components add to the mean-square speed, giving the factor one third.', '⟨vₓ²⟩ = ⟨v²⟩/3;  pV = ⅔N⟨Ktranslation⟩'),
    S('Supply the thermal relation', 'Classical equilibrium gives ½kBT per independent quadratic translational degree of freedom. Three directions give 3kBT/2 per molecule. This statistical input is additional to Newtonian collision mechanics.', '⟨Ktranslation⟩ = 3kBT/2 ⇒ pV = NkBT', ('Why exactly kBT/2 per quadratic degree of freedom?', 'equipartition')),
    S('Convert particles to moles', 'Use the definition of mole count and the relation between the two gas constants.', 'N = nNA;  R = NAkB ⇒ pV = nRT'),
  ], 'For one mole at 300 K in 0.025 m³, the ideal pressure is 8.314 × 300/0.025 ≈ 99.8 kPa.',
  '⟨v²⟩ is not ⟨v⟩². Newton’s laws alone do not establish the thermal energy–temperature relation.', ('Ideal Gas', 'Pressure, Temperature, and RMS Speed'))

T(19, 'adiabatic-gas', 'Derive pVᵞ = constant for an ideal gas', 'pVᵞ = constant;  TVᵞ⁻¹ = constant',
  'A reversible adiabatic gas cools as it does work using its own internal energy. Combining the first law with the ideal-gas equation fixes how its temperature and pressure change.',
  'CV, CP: molar heat capacities; γ = CP/CV; n: fixed mole count; Wby: work by the gas.',
  'Ideal gas, reversible adiabatic path, pressure–volume work only, and approximately constant heat capacities over the temperature range.', [
    S('Apply the adiabatic first law', 'With no heat crossing the boundary, the energy lost equals the work done. Reversibility lets us use the gas pressure for boundary work.', 'nCV dT = −p dV', ('Where does this work expression come from?', 'first-law')),
    S('Use the ideal-gas pressure', 'Replace p by nRT/V and divide by nCVT. This separates temperature and volume.', 'dT/T = −(R/CV)dV/V'),
    S('Identify the heat-capacity ratio', 'For an ideal gas, heating at constant pressure requires additional expansion work R dT per mole, so CP = CV + R. Thus R/CV = γ − 1.', 'ln(Tf/Ti) = −(γ − 1)ln(Vf/Vi)'),
    S('Exponentiate and eliminate temperature', 'The logarithmic relation gives TVᵞ⁻¹ constant. Using T = pV/(nR) produces the pressure–volume form.', 'TiViᵞ⁻¹ = TfVfᵞ⁻¹ ⇒ piViᵞ = pfVfᵞ'),
  ], 'For a monatomic ideal gas with γ = 5/3, doubling volume reversibly and adiabatically reduces temperature to 2⁻²ᐟ³ ≈ 0.630 of its initial value.',
  'Adiabatic alone is insufficient. Irreversible free expansion of an ideal gas is adiabatic but does not follow pVᵞ = constant.', ('Adiabatic Expansion of an Ideal Gas',))

T(20, 'entropy', 'Why entropy uses δQrev/T', 'dS = δQrev/T;  ΔS = ∫rev δQ/T',
  'Entropy is a state function whose differences are defined through reversible heat transfer divided by absolute temperature. The second law supplies the path-independence needed for this definition.',
  'S: thermodynamic entropy (J/K); δQrev: heat entering on a reversible reference path; T: absolute temperature along that path.',
  'Equilibrium endpoints and a reversible connecting path for the integral. The actual process need not be reversible.', [
    S('State the required theorem', 'For any reversible cycle, Clausius’s equality says that the closed integral of δQrev/T is zero. This follows from the second law through reversible-engine arguments.', '∮rev δQ/T = 0', ('Prove the reversible-cycle equality', 'clausius')),
    S('Turn a zero cyclic integral into a state difference', 'Follow one reversible path from A to B and another back from B to A. Zero integral around the combined cycle means that the two A-to-B integrals agree. Their common value defines SB − SA.'),
    S('Integrate with the temperature actually varying along the reference path', 'Only when the heat transfer is reversible and isothermal can T be taken outside the integral.', 'ΔSisothermal,rev = Qrev/T'),
    S('Treat an irreversible process using different bookkeeping', 'For an actual closed-system process, entropy transfer with heat and internal entropy production must both be counted. Boundary temperature Tb is used for the heat transfer.', 'ΔS = ∫actual δQ/Tb + Sgenerated;  Sgenerated ≥ 0'),
    S('Compute an ideal-gas state difference', 'Use a convenient reversible path and the first law with dU = nCV dT. For constant CV, integrating temperature and volume terms gives a state formula.', 'ΔS = nCV ln(Tf/Ti) + nR ln(Vf/Vi)'),
  ], 'An insulated ideal gas freely expanding to twice its volume keeps the same temperature and has ΔS = nR ln 2 > 0, although actual Q = 0.',
  'ΔS = Q/T is not a general formula for arbitrary heat and processes. A reversible reference path is essential to the definition.', ('Entropy', 'Change in Entropy'))

T(20, 'carnot', 'Derive the Carnot heat ratio and efficiency', 'Qc/Qh = Tc/Th;  ηCarnot = 1 − Tc/Th',
  'A reversible Carnot cycle has two isothermal and two adiabatic legs. For an ideal-gas working substance, matching the adiabatic endpoints makes the isothermal volume ratios equal, producing the heat ratio.',
  'Th > Tc: absolute reservoir temperatures; Qh > 0: heat absorbed; Qc > 0: heat rejected in magnitude; Wout: net cycle work.',
  'Reversible engine between two reservoirs. The explicit working-substance calculation uses a fixed amount of ideal gas with constant heat capacities.', [
    S('Label the four states in order', 'Let 1→2 be isothermal expansion at Th, 2→3 adiabatic expansion to Tc, 3→4 isothermal compression at Tc, and 4→1 adiabatic compression to Th.'),
    S('Calculate each isothermal heat magnitude', 'An ideal gas has no internal-energy change along an isotherm. Therefore the heat magnitude equals the reversible isothermal work magnitude.', 'Qh = nRTh ln(V₂/V₁);  Qc = nRTc ln(V₃/V₄)', ('Derive the logarithmic work formula', 'isothermal-work')),
    S('Use the two adiabatic constraints', 'On 2→3 and 4→1, TVᵞ⁻¹ is constant. Dividing the two relations cancels the temperatures, so V₂/V₁ = V₃/V₄.', 'ThV₂ᵞ⁻¹ = TcV₃ᵞ⁻¹;  ThV₁ᵞ⁻¹ = TcV₄ᵞ⁻¹', ('Derive the adiabatic relation', 'adiabatic-gas')),
    S('Cancel the identical logarithms', 'The heat formulas contain the same dimensionless volume ratio, leaving only the temperature ratio. No entropy definition was used in this calculation.', 'Qc/Qh = Tc/Th'),
    S('Apply energy conservation over a cycle', 'The internal energy returns to its starting value, so net output is Qh − Qc. Efficiency is that output divided by the input heat. The second law makes the reversible result universal, independent of the working substance.', 'η = Wout/Qh = 1 − Qc/Qh = 1 − Tc/Th', ('Why is the reversible heat ratio universal?', 'clausius')),
  ], 'For Th = 600 K and Tc = 300 K, the reversible efficiency is 50%. An engine absorbing 1000 J rejects 500 J and produces 500 J of work per cycle.',
  'Qc here is a positive magnitude. Using signed heat into the working substance, the cold-leg heat is −Qc. Temperatures must be kelvin.', ('A Carnot Engine', 'Efficiency'))

T(21, 'coulomb', 'Coulomb’s law and superposition', '𝐅₁←₂ = ke q₁q₂(𝐫₁ − 𝐫₂)/|𝐫₁ − 𝐫₂|³',
  'Coulomb’s inverse-square law is an empirical electrostatic law, not an algebraic theorem. Its vector form encodes attraction or repulsion, and superposition builds the force from several charges.',
  'q₁, q₂: signed charges (C); 𝐫₁, 𝐫₂: their positions; ke = 1/(4πε₀); 𝐅₁←₂: force on charge 1 from charge 2.',
  'Stationary point charges in vacuum, or spherical distributions used only where the point-charge equivalence applies.', [
    S('State the measured magnitude law', 'The magnitude is proportional to the product of charge magnitudes and inversely proportional to their separation squared.', 'F = ke|q₁q₂|/r²'),
    S('Supply a direction', 'The unit vector from charge 2 toward charge 1 is (𝐫₁ − 𝐫₂)/r. Multiplying it by keq₁q₂/r² gives repulsion for equal signs and attraction for opposite signs.', 'r = |𝐫₁ − 𝐫₂|'),
    S('Add independent contributions', 'Electrostatic superposition states that the total force is the vector sum of the pairwise forces. Resolve into components when the charges are not collinear.', '𝐅net,on 1 = Σj≠1 𝐅₁←ⱼ', ('How are vector forces added?', 'vector-components')),
    S('Pass to a continuous charge distribution', 'Replace the point-source sum by a charge integral. Each source element dq contributes along its own displacement direction.', '𝐅on q = keq ∫ (𝐫 − 𝐫′) dq/|𝐫 − 𝐫′|³'),
  ], 'Two charges +1 μC and −2 μC separated by 0.10 m attract with force magnitude about 1.80 N using ke ≈ 8.99 × 10⁹ N·m²/C².',
  'Do not add force magnitudes before accounting for direction. A scalar product of signed charges in the magnitude formula requires an absolute value.', ('Coulomb’s Law',))

T(21, 'charge-conservation', 'Charge conservation and quantization', 'q = ne;  Σqbefore = Σqafter',
  'Charge quantization and conservation are physical principles. They constrain what processes can occur; they are not derived from the inverse-square force law.',
  'e > 0: elementary charge magnitude, exactly 1.602176634 × 10⁻¹⁹ C; n: integer for ordinary isolated composite objects; electron charge is −e.',
  'For q = ne as used here, consider ordinary isolated objects built from electrons and nuclei. Quarks carry fractional elementary charges but are not observed as isolated free particles.', [
    S('Separate charge from particle count', 'Electrons and protons carry equal-magnitude opposite charges. An object is neutral when their total charges cancel, not when it contains no charged constituents.', 'q = (Np − Ne)e'),
    S('Transfer electrons between objects', 'Moving one electron from A to B raises A’s charge by e and lowers B’s by e. The individual charges change but their sum does not.', 'ΔqA = +e;  ΔqB = −e'),
    S('Apply conservation to a closed system', 'No charge entering or leaving means the net charge is constant. If charge crosses the boundary, the rate of charge loss equals the outward current.', 'dQinside/dt = −Iout', ('How does current measure transported charge?', 'current-drift')),
    S('Use net charge in an interaction law', 'Once the charges and geometry are known, a force law predicts interactions. Conservation alone neither sets force strength nor determines where the charges sit.', 'F = ke|q₁q₂|/r²', ('How do the charges determine a force?', 'coulomb')),
  ], 'Removing 10¹² electrons from a neutral object leaves charge +1.602 × 10⁻⁷ C. The removed electrons together carry the opposite charge.',
  'Conservation applies to net signed charge. Particle creation can produce oppositely charged pairs without changing that net charge.', ('Charge Is Quantized', 'Charge Is Conserved'))

T(22, 'electric-field', 'Derive the field on the axis of a charged ring', 'Eaxis = keQz/(z² + R²)³ᐟ²',
  'An electric field is force per unit positive test charge. For a uniformly charged ring, symmetry cancels transverse field components while the axial components add.',
  'Q: total ring charge; R: ring radius; z: signed axial position measured from the ring centre; Eaxis: signed axial component.',
  'Uniform thin ring of charge in electrostatics and vacuum. The observation point lies on the ring axis.', [
    S('Define electric field independently of a test charge', 'For a sufficiently small test charge q, field is the force divided by q. Coulomb’s law gives a source element’s field.', '𝐄 = 𝐅/q;  dE = ke dq/(R² + z²)', ('State the source force law', 'coulomb')),
    S('Use rotational symmetry', 'Opposite ring elements contribute equal and opposite transverse components at an axial observation point. Their axial components have the same direction for a given signed z and Q.'),
    S('Project each contribution', 'The element-to-point distance is √(R² + z²). The cosine of its angle to the axis is z divided by that distance.', 'dEaxis = ke z dq/(R² + z²)³ᐟ²'),
    S('Integrate around the ring', 'At a fixed axial point, the geometric factor is constant over the ring. The integral of dq is the total charge Q.', 'Eaxis = [ke z/(R² + z²)³ᐟ²] ∫dq'),
  ], 'At z = 0 the field vanishes by symmetry. Far from the ring, |z| ≫ R, the expression approaches the field of a point charge Q.',
  'This axial result does not describe points off the axis. Zero field at the centre does not imply zero potential there.', ('Electric Field', 'The Electric Field Due to a Charged Ring'))

T(22, 'electric-dipole', 'Derive the torque and energy of an electric dipole', '𝛕 = 𝐩 × 𝐄;  U = −𝐩 · 𝐄',
  'A neutral pair of separated opposite charges can experience zero net force in a uniform field yet still rotate. Its dipole moment describes that turning effect.',
  '𝐩 = q𝐝: dipole moment, directed from −q to +q; 𝐄: external field; θ: angle between them.',
  'A rigid dipole in an approximately uniform electrostatic external field. The constant in potential energy is chosen so U = 0 at θ = 90°.', [
    S('Add the two forces', 'The positive charge feels q𝐄 and the negative charge feels −q𝐄. The net force is zero when the same field acts at both ends.', '𝐅net = q𝐄 − q𝐄 = 0'),
    S('Add the torques about the centre', 'Each charge has a lever arm of d/2. Both forces turn the dipole in the same rotational sense, toward alignment.', 'τmagnitude = 2(qE)(d/2)sin θ = pE sin θ'),
    S('Identify the vector direction', 'The right-hand rule gives the torque vector. For a signed angle increasing away from alignment, the rotational component is restoring: τθ = −pE sin θ.', '𝛕 = 𝐩 × 𝐄', ('Why is torque a cross product?', 'angular-momentum')),
    S('Integrate the torque to obtain energy', 'Use τθ = −dU/dθ. Then dU = pE sin θ dθ, whose integral is −pE cos θ plus an arbitrary constant.', 'U = −pE cos θ = −𝐩 · 𝐄'),
  ], 'A dipole with p = 2 × 10⁻⁶ C·m in E = 1000 N/C has maximum torque 0.002 N·m. Rotating it slowly from aligned to anti-aligned requires 0.004 J.',
  'A nonuniform field can also exert a net dipole force. The uniform-field zero-force conclusion then no longer applies.', ('A Dipole in an Electric Field',))

T(23, 'gauss-sphere', 'Use Gauss’s law to derive a spherical electric field', '∮𝐄 · d𝐀 = Qenc/ε₀;  Eoutside = Q/(4πε₀r²)',
  'Gauss’s law is a general field law. Spherical symmetry is the additional ingredient that lets us extract a local electric field from the total flux.',
  'Qenc: enclosed charge; d𝐀: outward-oriented surface-area element; r: Gaussian-sphere radius; ε₀: vacuum permittivity.',
  'Electrostatics in vacuum. The simple field evaluation requires a spherically symmetric charge distribution centred on the Gaussian sphere.', [
    S('Distinguish flux from field', 'Flux adds the normal component of electric field over a closed surface. Gauss’s law fixes that total using enclosed charge; it does not imply that field is constant on an arbitrary surface.', 'ΦE = ∮𝐄 · d𝐀 = Qenc/ε₀'),
    S('Choose a sphere matching the symmetry', 'Spherical symmetry requires a radial field with the same signed radial component everywhere on a concentric sphere. It can therefore be taken out of the surface integral.', 'ΦE = Er(r) ∮dA = Er(r)4πr²'),
    S('Evaluate the exterior field', 'Outside the entire distribution, the enclosed charge is Q. Divide the flux relation by the sphere area.', 'Er(r) = Q/(4πε₀r²)', ('How does this match Coulomb’s law?', 'coulomb')),
    S('Evaluate the interior of a uniform solid sphere', 'For sphere radius R, the enclosed fraction of charge is r³/R³. Substitution gives a field proportional to r inside.', 'Qenc = Qr³/R³ ⇒ Er = Qr/(4πε₀R³)  (r < R)'),
  ], 'At r = 0 the uniform solid sphere has zero field. At r = R the interior and exterior formulas agree.',
  'Zero enclosed charge implies zero net flux, not necessarily zero field. External charges can produce nonzero fields whose inward and outward fluxes cancel.', ('Gauss’ Law',))

T(23, 'gauss-cylinder-plane', 'Derive fields of an infinite line and sheet', 'Eline = |λ|/(2πε₀r);  Esheet = |σ|/(2ε₀)',
  'For highly symmetric sources, choose a Gaussian surface on which the normal field is either constant or zero. This turns a surface integral into field magnitude times a known area.',
  'λ: charge per length; σ: charge per area; r: perpendicular distance from the infinite line. Displayed E values are magnitudes.',
  'Infinite straight line or infinite uniform nonconducting sheet in vacuum. Large finite objects approximate these near their middle, away from edges.', [
    S('Choose a cylindrical surface for the line', 'The field is radial and constant on a coaxial cylinder of radius r and length ℓ. The end caps have zero flux because their area vectors are parallel to the line.', 'ΦE = E(2πrℓ);  |Qenc| = |λ|ℓ'),
    S('Apply Gauss’s law to the line', 'Divide enclosed-charge-over-permittivity by the cylinder’s side area. Length cancels, leaving an inverse-distance field.', 'Eline = |λ|/(2πε₀r)', ('Why may the field leave the integral?', 'gauss-sphere')),
    S('Choose a pillbox crossing the sheet', 'Reflection symmetry gives equal field magnitudes on both sides, normal to the plane. The side has no flux; each flat cap contributes EA.', 'ΦE = 2EA;  |Qenc| = |σ|A'),
    S('Apply Gauss’s law to the sheet', 'Area cancels. An infinite sheet has a distance-independent field on either side; two opposite sheets superpose to give σ/ε₀ between them.', 'Esheet = |σ|/(2ε₀)'),
  ], 'Two large oppositely charged plates with |σ| = 10⁻⁶ C/m² have an interior field about 1.13 × 10⁵ N/C when edge effects are negligible.',
  'A conductor’s surface relation Eoutside = σ/ε₀ uses zero interior field and one exterior cap. It differs from an isolated nonconducting sheet.', ())

T(24, 'electric-potential', 'Derive potential from an electric field', 'Vb − Va = −∫ₐᵇ 𝐄 · d𝐥;  Vpoint = keQ/r',
  'Electric potential is potential energy per unit test charge. Its spatial change encodes the work per charge performed by an electrostatic field.',
  'V: electric potential (J/C); 𝐄: electrostatic field; Q: source point charge; r: distance to it; 𝐥: path coordinate.',
  'Electrostatic conservative field. For an isolated point charge choose zero potential at infinity.', [
    S('Relate electric work and potential energy', 'A test charge q feels force q𝐄. Its conservative work over a path is q times the field integral, and the potential-energy change is minus that work.', 'ΔU = −q ∫ₐᵇ 𝐄 · d𝐥', ('Why does potential energy use minus work?', 'potential-energy')),
    S('Divide out the test charge', 'Defining V = U/q makes the potential a property of the source field rather than the test charge used to probe it.', 'ΔV = −∫ₐᵇ 𝐄 · d𝐥'),
    S('Integrate a point-charge field', 'For radial travel, Er = keQ/r². Integrate from infinity to r, keeping Q signed.', 'V(r) = −∫∞ʳ keQ/r′² dr′ = keQ/r'),
    S('Reverse the construction', 'For a tiny displacement along x, dV = −Eₓ dx. Thus the field is minus the spatial derivative of potential; in three dimensions it is the negative gradient.', 'Eₓ = −∂V/∂x;  𝐄 = −∇V'),
  ], 'A positive charge moving along the field through a potential drop of 10 V loses 10 J of electric potential energy per coulomb.',
  'Potential is a signed scalar and can cancel when fields do not. A time-varying magnetic field requires more than a scalar electrostatic potential.', ('Electric Potential', 'Calculating the Potential from the Field'))

T(24, 'electric-energy', 'Build the potential energy of a charge arrangement', 'U = Σi<j keqiqj/rij = ½Σi qiVothers(𝐫i)',
  'The energy of a charge configuration is the work needed to assemble it slowly from a chosen reference of infinitely separated charges. Each interacting pair is counted once.',
  'qi: signed point charges; rij: pair separations; Vothers: potential due to all charges other than the charge at the evaluation point.',
  'Static point charges in vacuum, quasistatic assembly, and finite pair separations. Self-energies of ideal point charges are excluded.', [
    S('Bring in the first charge', 'With no other charges present, there is no interaction energy to overcome. Choose this contribution as zero.'),
    S('Bring in the second charge', 'The first charge creates potential keq₁/r₁₂ at the second location. Quasistatic external work equals the potential-energy increase.', 'U₁₂ = q₂V₁ = keq₁q₂/r₁₂', ('Derive point-charge potential', 'electric-potential')),
    S('Add more charges', 'Each newly brought charge interacts with those already present. Summing this construction counts every unordered pair once.', 'Uthree = ke(q₁q₂/r₁₂ + q₁q₃/r₁₃ + q₂q₃/r₂₃)'),
    S('Understand the factor one half', 'The sum ΣqiVothers at all charge locations counts pair i–j once from i and once from j. Divide by two to correct this duplication.', 'U = ½Σi qiVothers(𝐫i)'),
  ], 'Two charges +1 μC and −1 μC at 0.10 m have U ≈ −0.0899 J. Separating them to infinity requires positive external work 0.0899 J.',
  'Never include a point charge’s own divergent potential when computing Vothers. Negative U means lower energy than the chosen separated reference.', ('Electric Potential Energy of a System of Point Charges',))

T(25, 'parallel-plate-capacitance', 'Derive parallel-plate capacitance', 'C = Q/ΔV = εA/d',
  'Capacitance relates the charge separated on two conductors to their potential difference. Parallel plates permit a direct derivation from their nearly uniform electric field.',
  'Q > 0: charge magnitude on either plate; A: facing area; d: separation; ε: uniform filling-medium permittivity; C: capacitance (F).',
  'Large parallel conducting plates, d much smaller than lateral dimensions, negligible fringing, and a uniform linear dielectric filling the gap.', [
    S('Find the surface charge density', 'With charges +Q and −Q spread uniformly over the facing areas, the magnitude is σ = Q/A.', 'σ = Q/A'),
    S('Find the field in the gap', 'The two plate fields add inside and approximately cancel outside. In vacuum E = σ/ε₀; a homogeneous linear dielectric replaces ε₀ by ε.', 'E = Q/(εA)', ('Why do two plate fields add to σ/ε₀?', 'gauss-cylinder-plane')),
    S('Integrate field over separation', 'Because the gap field is approximately uniform, the magnitude of the potential difference is Ed.', 'ΔV = Ed = Qd/(εA)'),
    S('Apply the definition of capacitance', 'Divide Q by ΔV. For this linear medium, charge cancels and the result depends on geometry and permittivity.', 'C = Q/ΔV = εA/d'),
  ], 'Vacuum plates of area 0.010 m² separated by 1.0 mm have capacitance 8.85 × 10⁻¹¹ F, about 88.5 pF.',
  'At fixed battery voltage, adding a dielectric draws extra charge. For disconnected plates, charge stays fixed and voltage falls.', ('Capacitor; Capacitance', 'Calculating the Capacitance'))

T(25, 'capacitor-energy', 'Derive energy stored in a capacitor', 'U = Q²/(2C) = ½QΔV = ½C(ΔV)²',
  'Charging a capacitor becomes progressively harder as its voltage rises. Integrating the small work needed to transfer each increment of charge gives the factor one half.',
  'C: constant capacitance; q: temporary charge magnitude during charging; Q: final charge magnitude; ΔV: final voltage magnitude.',
  'A linear capacitor with constant geometry and permittivity, charged quasistatically from zero charge. This calculates stored energy rather than circuit dissipation.', [
    S('Track the voltage while charging', 'At an intermediate charge q, the voltage is q/C, not its eventual final value.', 'ΔV(q) = q/C'),
    S('Transfer a small additional charge', 'Moving dq against that potential difference requires differential work ΔV(q)dq. Reversible charging stores it as field energy.', 'dU = (q/C)dq'),
    S('Integrate from empty to full', 'The integral of q gives Q²/2. Substitute Q = CΔV to obtain the equivalent forms.', 'U = ∫₀Q (q/C)dq = Q²/(2C)', ('Why does a linearly growing quantity give a factor ½?', 'integrals')),
    S('Express it as field energy density', 'For parallel plates, use C = εA/d and ΔV = Ed. The resulting total energy is proportional to the gap volume Ad.', 'U = ½εE²(Ad) ⇒ uE = ½εE²'),
  ], 'A 10 μF capacitor at 12 V stores ½ × 10⁻⁵ × 144 = 0.00072 J.',
  'A fixed-voltage source supplies QΔV during simple resistive charging; only half is finally stored in an initially empty ideal capacitor.', ('Potential Energy and Energy Density',))

T(26, 'current-drift', 'Derive current from carrier drift', 'I = nqAvd;  𝐉 = nq𝐯d',
  'Current counts how much net charge crosses a surface per unit time. A slow average drift of many carriers can produce a substantial current even though their random motion mostly cancels.',
  'n: carrier number density (m⁻³); q: signed charge per carrier; A: cross-sectional area; 𝐯d: mean drift velocity; 𝐉: current density.',
  'Uniform steady flow of one carrier species. The scalar magnitude formula uses |q| and the positive drift-speed magnitude.', [
    S('Define current as charge rate', 'Choose a positive surface direction. Net charge transported through the section determines signed current.', 'I = dQ/dt'),
    S('Count crossing carriers', 'During dt, carriers drifting distance vd dt sweep a volume Avd dt. Multiply this by number density to obtain the number crossing.', 'dN = nAvd dt'),
    S('Convert carrier count to charge', 'Each carrier contributes charge q. Dividing the transported charge by dt gives the current; the vector form includes carrier direction.', 'dQ = qdN ⇒ 𝐉 = nq𝐯d'),
    S('Account for negative carriers', 'For electrons q is negative. Their drift velocity points opposite conventional current, so the product q𝐯d points along the current density. Add separate nq𝐯d terms if multiple species conduct.'),
  ], 'For n = 8.5 × 10²⁸ m⁻³, A = 10⁻⁶ m² and current 1 A, electron drift-speed magnitude is about 7.3 × 10⁻⁵ m/s.',
  'Drift speed is not the speed of the electrical signal and is not the electrons’ much larger random microscopic speed.', ('Current', 'Drift Speed of the Charge Carriers'))

T(26, 'resistance', 'Derive R = ρL/A and Joule heating', 'R = ρL/A;  P = IΔV = I²R = (ΔV)²/R',
  'A material’s local response to electric field determines its resistivity. Geometry converts that local relation into the terminal resistance of a wire, while energy per transported charge gives electrical power.',
  'ρ: electrical resistivity (Ω·m), not mass density here; L: wire length; A: cross section; σ = 1/ρ: conductivity.',
  'Uniform straight ohmic conductor at fixed temperature, approximately uniform field and current density. The heating formulas concern a resistive voltage drop.', [
    S('State the local material model', 'Ohm’s local law says current density is proportional to electric field. The proportionality is a measured material property.', '𝐉 = σ𝐄;  E = ρJ'),
    S('Relate local quantities to terminal ones', 'For a uniform wire, current density is I/A and the voltage-drop magnitude is EL.', 'ΔV = EL = ρ(I/A)L'),
    S('Identify resistance', 'Defining R = ΔV/I gives the geometry dependence. A longer wire has more resistance; a larger cross section provides more parallel conducting area.', 'R = ρL/A'),
    S('Derive power from transferred energy', 'A charge increment dQ passing through a voltage drop releases energy ΔV dQ. Divide by time and use I = dQ/dt, then substitute Ohm’s law.', 'P = ΔV(dQ/dt) = IΔV = I²R', ('Why is current a charge rate?', 'current-drift')),
  ], 'A 2 Ω resistor carrying 3 A has a 6 V drop and dissipates 18 W. If its resistance is unchanged and voltage doubles, power quadruples.',
  'R = ΔV/I can be defined for a device, but constant R is the extra ohmic assumption. Heating can change resistivity and resistance.', ('Resistance and Resistivity', 'Power in Electric Circuits'))

T(27, 'kirchhoff', 'Derive Kirchhoff rules and equivalent resistance', 'ΣIin = ΣIout;  Σloop ΔV = 0',
  'The junction rule is charge conservation for an ideal circuit node. The ordinary loop rule expresses the balance of potential changes around a lumped circuit with no unaccounted changing magnetic flux.',
  'I: signed branch currents; R: ideal resistances; ℰ: source emf; ΔV: signed potential change when traversing an element.',
  'Lumped, quasisteady circuit model; negligible charge accumulation at ideal nodes. Induced emf must be explicitly included if linked magnetic flux changes.', [
    S('Apply conservation at a node', 'If charge is not building up at a junction, the charge arriving each second equals the charge leaving.', 'ΣIin − ΣIout = dQnode/dt = 0'),
    S('Return to the same potential', 'Traverse a closed loop and add signed changes. A resistor traversed along the assigned current contributes −IR; an ideal source traversed from minus to plus contributes +ℰ.', 'Σloop ΔV = 0'),
    S('Combine resistors in series', 'The same current passes through each resistor, and voltage drops add. Dividing total drop by current gives the equivalent resistance.', 'Req,series = R₁ + R₂ + …', ('Where does the resistor voltage relation come from?', 'resistance')),
    S('Combine resistors in parallel', 'Branches share the same voltage, while their currents add. Substitute Ii = ΔV/Ri into the junction rule.', '1/Req,parallel = 1/R₁ + 1/R₂ + …'),
  ], 'A 6 Ω resistor in parallel with 3 Ω has equivalent resistance 2 Ω. At 12 V their branch currents are 2 A and 4 A, totaling 6 A.',
  'A negative solved current means actual flow opposes the assigned arrow. It does not invalidate the chosen equation system.', ('The Junction Rule', 'The Loop Rule'))

T(27, 'rc-circuit', 'Derive exponential charging of an RC circuit', 'q(t) = Cℰ(1 − e⁻ᵗᐟᴿᶜ);  I(t) = (ℰ/R)e⁻ᵗᐟᴿᶜ',
  'As a capacitor charges, its increasing voltage leaves less source voltage across the resistor. That feedback makes the current and the remaining charge deficit decay exponentially.',
  'R: series resistance; C: capacitance; ℰ: ideal constant emf; q: capacitor charge magnitude; τ = RC: time constant.',
  'Ideal series resistor and capacitor, a suddenly connected DC source, initially uncharged capacitor, constant R and C.', [
    S('Apply the loop rule', 'The source rise equals resistor drop plus capacitor drop. Current is the rate at which charge accumulates on the plate.', 'ℰ − RI − q/C = 0;  I = dq/dt', ('Why must circuit voltage changes balance?', 'kirchhoff')),
    S('Write the differential equation', 'Rearrange so the rate is proportional to the deficit between q and its final value Cℰ.', 'dq/dt = (Cℰ − q)/(RC)'),
    S('Separate and integrate', 'Let u = Cℰ − q. Its derivative is −u/(RC), whose logarithmic integral gives an exponential. Initial charge zero makes u(0) = Cℰ.', 'u(t) = Cℰ e⁻ᵗᐟᴿᶜ ⇒ q(t) = Cℰ(1 − e⁻ᵗᐟᴿᶜ)'),
    S('Differentiate to get current', 'The derivative decays from ℰ/R to zero. The capacitor voltage approaches ℰ, so the final resistor drop vanishes.', 'I(t) = dq/dt = (ℰ/R)e⁻ᵗᐟᴿᶜ'),
  ], 'With R = 1000 Ω and C = 100 μF, τ = 0.10 s. At t = τ the capacitor has reached 1 − e⁻¹ ≈ 63.2% of its final charge.',
  'The capacitor does not instantly reach full charge. Its initial charging current is nonzero, while its initial voltage is zero in this setup.', ('RC Circuits',))

T(28, 'magnetic-orbit', 'Derive a charged particle’s magnetic orbit radius', 'r = mv⊥/(|q|B);  ωc = |q|B/m',
  'Magnetic force bends velocity without doing work on a point charge. In a uniform magnetic field the perpendicular part of motion is circular, while any parallel component continues unchanged.',
  'q: particle charge; m: mass; B: field magnitude; v⊥: velocity component perpendicular to the field; ωc: cyclotron angular frequency.',
  'Uniform time-independent magnetic field, no electric field or other significant forces, nonrelativistic particle.', [
    S('State the magnetic part of the Lorentz force', 'The cross product gives a force perpendicular to both velocity and field. Its magnitude uses only v⊥.', '𝐅B = q𝐯 × 𝐁;  FB = |q|v⊥B'),
    S('Check the work rate', 'The force is perpendicular to the full velocity, so its dot product with velocity vanishes. The speed and kinetic energy stay constant.', 'P = 𝐅B · 𝐯 = 0', ('Why is power force dotted with velocity?', 'work-energy')),
    S('Supply centripetal acceleration', 'In the plane normal to the field, magnetic force provides the inward force for circular motion. Equate magnitudes.', '|q|v⊥B = mv⊥²/r', ('Derive the required inward acceleration', 'centripetal-acceleration')),
    S('Solve radius and frequency', 'Cancel one v⊥ to find r. The angular frequency v⊥/r then loses its speed dependence in the nonrelativistic model.', 'r = mv⊥/(|q|B);  ωc = v⊥/r = |q|B/m'),
  ], 'A proton with v⊥ = 10⁶ m/s in B = 0.10 T has radius about 0.104 m. Adding a parallel velocity changes the path into a helix.',
  'The sign of charge changes the turning direction. At relativistic speeds use relativistic momentum: r = p⊥/(|q|B).', ('A Circulating Charged Particle',))

T(28, 'magnetic-wire', 'Derive force and torque on a current loop', 'd𝐅 = I d𝐥 × 𝐁;  𝛕 = 𝛍 × 𝐁;  μ = NIA',
  'A current consists of moving charge, so the magnetic force on its carriers becomes a force on the conductor. Opposite sides of a loop can form a turning couple.',
  'I: conventional current; d𝐥: wire element along current; N: loop turns; A: one turn’s area; 𝛍: magnetic dipole moment normal by the right-hand rule.',
  'Thin wire in a prescribed magnetic field. The simple dipole torque formula uses a uniform field and a planar loop.', [
    S('Add carrier forces in a segment', 'For carrier density n, charge q and segment volume Awdℓ, the total force is nqAwdℓ 𝐯d × 𝐁. Recognize current I = nqAwvd with its conventional direction.', 'd𝐅 = I d𝐥 × 𝐁', ('Derive current from carrier drift', 'current-drift')),
    S('Evaluate a straight segment', 'When field and wire direction are constant, integrate d𝐥 to the length vector. The cross product makes parallel segments feel no magnetic force.', '𝐅 = I𝐋 × 𝐁'),
    S('Find the turning couple of a rectangular loop', 'For loop sides a and b and normal tilted by θ from the field, opposite forces on the relevant sides have magnitude IaB and perpendicular separation b sin θ.', 'τ = (IaB)(b sin θ) = IAB sin θ'),
    S('Define the magnetic moment', 'Summing N identical turns multiplies torque by N. Assign the loop moment along the right-hand normal and write the vector law. Its energy is minimized when aligned.', '𝛍 = NIA n̂;  𝛕 = 𝛍 × 𝐁;  U = −𝛍 · 𝐁'),
  ], 'A 20-turn loop of area 0.010 m² carrying 0.50 A has μ = 0.10 A·m². In a 0.20 T field its maximum torque is 0.020 N·m.',
  'A closed loop in a uniform field has zero net force, yet may have nonzero torque. Nonuniform fields can also exert a net force.', ('Magnetic Force on a Current-Carrying Wire', 'Torque on a Current Loop'))

T(29, 'ampere-wire', 'Derive the magnetic field of a long straight wire', 'B = μ₀I/(2πr)',
  'Ampère’s law fixes magnetic circulation around a steady current. Cylindrical symmetry makes the field tangent to a circle and constant in magnitude on it.',
  'I: enclosed steady current; r: perpendicular distance from a very long straight wire; μ₀: vacuum permeability.',
  'Magnetostatic current in an effectively infinite straight wire in vacuum. The exterior formula is used outside the wire radius.', [
    S('State the circulation law', 'For steady currents, the closed line integral of magnetic field is μ₀ times the current threading the loop.', '∮𝐁 · d𝐥 = μ₀Ienc'),
    S('Choose a symmetry-matched loop', 'The field wraps around the wire according to the right-hand rule. On a coaxial circle of radius r, it is tangent and has constant magnitude.'),
    S('Evaluate the line integral', 'Every element contributes B dℓ with the same sign around the chosen direction. The circumference is 2πr.', 'B(2πr) = μ₀I ⇒ B = μ₀I/(2πr)'),
    S('Contrast the inside of a uniform wire', 'If current density is uniform in a wire of radius R, a smaller circle encloses I r²/R². The interior field grows linearly instead of diverging.', 'Binside = μ₀Ir/(2πR²)  (r < R)'),
  ], 'A 10 A straight wire gives about 2.0 × 10⁻⁴ T at r = 1 cm in vacuum.',
  'Ampère’s law is always a circulation statement, but extracting B this way requires symmetry. A nearby return wire can spoil the single-wire approximation.', ('Ampere’s Law',))

T(29, 'solenoid', 'Derive the ideal solenoid field', 'Binside ≈ μ₀nI;  Boutside ≈ 0',
  'A long tightly wound solenoid has an approximately uniform axial field inside. An Ampèrian rectangle converts that geometry into a simple relation between field and turns per length.',
  'n = N/ℓ: turn density; I: coil current; ℓ: winding length; B: magnetic flux-density magnitude.',
  'Very long, closely wound solenoid with steady current and an air or vacuum core, evaluated well away from the ends.', [
    S('Describe the ideal symmetry', 'In the infinite-solenoid limit, the field is axial and constant inside; the exterior field vanishes. A finite long solenoid approximates this near its middle.'),
    S('Draw a rectangular integration loop', 'One long side of length a lies inside parallel to the field, and the other lies outside. The short sides are perpendicular to the field and add no circulation.'),
    S('Count threaded current', 'The loop encloses na turns, each carrying I. Ampère’s law therefore sets its circulation to μ₀naI.', '∮𝐁 · d𝐥 ≈ Binside a = μ₀(na)I', ('How is Ampère’s law evaluated with symmetry?', 'ampere-wire')),
    S('Cancel loop length', 'The arbitrary integration length a disappears, leaving the field determined by current and turn density.', 'Binside ≈ μ₀nI'),
  ], 'For n = 1000 turns/m and I = 2 A, the ideal interior field is about 2.51 mT.',
  'The field near the ends is not uniform and the external field is not exactly zero for a finite coil. Magnetic cores require a material-response model.', ('Solenoids and Toroids',))

T(30, 'faraday', 'Faraday’s law, Lenz’s law, and motional emf', 'ℰ = −N dΦB/dt;  |ℰrod| = Bℓv',
  'Faraday’s law is the empirical connection between changing magnetic flux and induced emf. The sign specifies the sense of circulation that opposes the flux change, once loop orientation is chosen.',
  'ΦB = ∫𝐁 · d𝐀: flux per turn; N: identical turns; ℰ: loop emf; ℓ: rod length; v: rod speed.',
  'For the rod formula, a straight rod, velocity and magnetic field are mutually perpendicular and the rod forms part of a specified circuit.', [
    S('Choose a consistent loop orientation', 'The right-hand rule links positive circulation around the loop to a positive surface normal. Flux is signed using that normal.', 'ΦB = ∫surface 𝐁 · d𝐀'),
    S('State the induction law', 'For a stationary loop, changing field creates a circulating electric field. More generally a moving circuit also includes the force per charge 𝐯wire × 𝐁.', 'ℰ = ∮(𝐄 + 𝐯wire × 𝐁) · d𝐥 = −dΦB/dt'),
    S('Apply it to a sliding rod', 'A rod of length ℓ moving at speed v changes circuit area at rate ℓv. In a uniform perpendicular field, the flux-change magnitude is Bℓv.', '|dΦB/dt| = Bℓv ⇒ |ℰ| = Bℓv'),
    S('Understand the energy sign', 'The induced current’s magnetic force opposes the driven rod motion in this resistive circuit. Maintaining motion requires external power that becomes electrical heating.', 'Fexternalv = ℰI = I²R  (steady ideal sliding-rod circuit)', ('Why does a resistor dissipate I²R?', 'resistance')),
  ], 'A 0.20 m rod moving at 3.0 m/s through a perpendicular 0.50 T field produces emf magnitude 0.30 V.',
  'Lenz’s law opposes the change of flux, not necessarily the original field. A steady flux produces no Faraday emf even if it is large.', ('Faraday’s Law of Induction', 'Lenz’s Law'))

T(30, 'inductor-energy', 'Derive inductance and magnetic energy storage', 'ℰL = −L dI/dt;  UB = ½LI²',
  'Current in a coil produces linked magnetic flux. A changing current changes that flux and induces a back emf. Work against this back emf stores energy in the magnetic field.',
  'L: inductance (H); I: current; NΦB: total flux linkage; UB: stored magnetic energy.',
  'Linear inductor with fixed geometry and constant L, negligible resistive losses for the stored-energy calculation.', [
    S('Define inductance through flux linkage', 'In a linear magnetic environment, the total linked flux is proportional to the coil current.', 'NΦB = LI'),
    S('Apply Faraday’s law', 'Differentiate the linkage. The minus sign describes the induced emf opposing the current change; under passive voltage convention the terminal voltage is vL = L dI/dt.', 'ℰL = −d(NΦB)/dt = −L dI/dt', ('Where does this induced emf come from?', 'faraday')),
    S('Compute the storage power', 'The power supplied against the back emf is vLI. Multiplying by dt gives the differential energy stored.', 'dUB = I(L dI/dt)dt = LI dI'),
    S('Integrate from zero current', 'For constant L, integrating the linear function of I gives the factor one half.', 'UB = ∫₀ᴵ LI′ dI′ = ½LI²'),
  ], 'An ideal 0.20 H inductor carrying 3 A stores 0.90 J. Current cannot jump instantly with finite applied voltage in this ideal model.',
  'A real coil also has resistance and may have nonlinear core behaviour. Then electrical input need not all become recoverable magnetic energy.', ('Inductance', 'Energy Stored in a Magnetic Field'))

T(31, 'lc-oscillations', 'Derive LC oscillation frequency', 'd²q/dt² + q/(LC) = 0;  ω₀ = 1/√(LC)',
  'An ideal LC circuit exchanges energy between a capacitor’s electric field and an inductor’s magnetic field. Its charge obeys the same harmonic equation as a mass on a spring.',
  'q: signed charge on a chosen capacitor plate; I = dq/dt under the chosen reference; L: inductance; C: capacitance.',
  'Ideal closed LC circuit, no resistance or radiation loss, constant L and C, no external driving after the initial energy is supplied.', [
    S('Write the loop equation', 'With consistent passive element signs, the capacitor and inductor voltage terms sum to zero.', 'q/C + L dI/dt = 0'),
    S('Replace current with a charge rate', 'Differentiate q to obtain current, and differentiate again for the inductor term.', 'L d²q/dt² + q/C = 0'),
    S('Compare with harmonic motion', 'The coefficient of q is ω₀². Therefore q = Qmax cos(ω₀t + φ) solves the ideal circuit equation.', 'ω₀² = 1/(LC);  T = 2π√(LC)', ('Why does this equation have a sinusoidal solution?', 'simple-harmonic-motion')),
    S('Check energy exchange', 'When capacitor charge is largest current is zero, and vice versa. The sum of the two stored energies is constant.', 'U = q²/(2C) + ½LI² = constant'),
  ], 'For L = 0.10 H and C = 10 μF, ω₀ = 1000 rad/s and f ≈ 159 Hz.',
  'The current and charge are a quarter cycle out of phase. Real circuits damp unless driven because they dissipate energy.', ('LC Energy Transfers',))

T(31, 'ac-impedance', 'Derive impedance and resonance in a series RLC circuit', 'Z = √(R² + (ωL − 1/(ωC))²);  Imax = Vmax/Z',
  'In AC, inductor and capacitor voltages are out of phase with current. Their amplitudes cannot be added like DC resistor drops; their phase-aware sum gives impedance.',
  'ω: driving angular frequency; R, L, C: series circuit elements; Z: impedance magnitude (Ω); Vmax, Imax: sinusoidal peak amplitudes.',
  'Sinusoidal steady state in an ideal linear series RLC circuit with R > 0; transients have decayed.', [
    S('Take current as the phase reference', 'For I = Imax cos ωt, the resistor voltage follows I, the inductor voltage leads by 90°, and the capacitor voltage lags by 90°.', 'VR,max = ImaxR;  VL,max = ImaxωL;  VC,max = Imax/(ωC)'),
    S('Subtract opposite reactive contributions', 'The inductive and capacitive voltage phasors point opposite each other. Their difference is perpendicular in phase to the resistive voltage.', 'X = XL − XC = ωL − 1/(ωC)'),
    S('Find the amplitude of the sum', 'Apply Pythagoras in the phasor plane. Dividing total voltage amplitude by current amplitude defines the impedance magnitude.', 'Vmax² = (ImaxR)² + (ImaxX)² ⇒ Z = √(R² + X²)'),
    S('Set the reactive part to zero', 'At resonance the inductor and capacitor voltages cancel in their sum. The source then sees only R, and current amplitude is largest for a fixed voltage source.', 'ωres = 1/√(LC);  Zres = R', ('Why does the same LC frequency appear in free oscillation?', 'lc-oscillations')),
  ], 'For R = 30 Ω and net reactance X = 40 Ω, Z = 50 Ω. A 100 V peak source produces a 2 A peak current.',
  'Keep peak values and RMS values consistent. Average resistor power is Irms²R, which equals ½Imax²R.', ('Series RLC Circuits', 'Resonance'))

T(32, 'displacement-current', 'Why Maxwell added displacement current', '∮𝐁 · d𝐥 = μ₀(Iconduction + ε₀ dΦE/dt)',
  'A charging capacitor exposes a problem with the magnetostatic Ampère law: different surfaces spanning the same loop can intercept different conduction currents. The changing electric flux supplies the missing term.',
  'ΦE: electric flux through the chosen surface; Idisplacement = ε₀dΦE/dt in vacuum; Iconduction: actual charge transport through it.',
  'Vacuum Maxwell equations. The parallel-plate example neglects fringing and uses a quasistatic charging geometry.', [
    S('Span the same loop in two ways', 'One surface cuts the capacitor lead and intercepts conduction current I. Another bulges into the gap and intercepts no wire current. The circulation around the shared boundary must be the same.'),
    S('Compute the gap electric flux', 'For plates of area A with charge Q, E = Q/(ε₀A). The flux through the gap cross section is therefore Q/ε₀.', 'ΦE = EA = Q/ε₀', ('Derive the capacitor field', 'parallel-plate-capacitance')),
    S('Differentiate the flux', 'Multiplying its time derivative by ε₀ gives exactly dQ/dt, the current in the lead. This restores agreement for the two chosen surfaces.', 'ε₀dΦE/dt = dQ/dt = I'),
    S('State the general field law', 'Maxwell’s addition applies to changing electric fields generally, including vacuum regions with no conduction. The capacitor argument motivates its form but is not by itself a complete derivation of all electrodynamics.', '∮𝐁 · d𝐥 = μ₀Ienc + μ₀ε₀dΦE/dt'),
  ], 'If a parallel-plate capacitor is charging at 2 mA, its ideal full-gap displacement current is also 2 mA even though charge carriers do not cross the vacuum gap.',
  'Displacement current is a field term with current units; it is not ordinary charged particles travelling through empty capacitor space.', ('Induced Magnetic Fields', 'Displacement Current'))

T(32, 'em-wave-equation', 'Derive the electromagnetic wave speed from Maxwell’s equations', '∇²𝐄 = μ₀ε₀ ∂²𝐄/∂t²;  c = 1/√(μ₀ε₀)',
  'In empty space, a changing magnetic field curls the electric field, and a changing electric field curls the magnetic field. Combining the two laws yields a wave equation.',
  '𝐄, 𝐁: electric and magnetic fields; ∇×: curl; ∇·: divergence; ∇²: componentwise Laplacian.',
  'Source-free vacuum region with zero charge and conduction current, sufficiently smooth fields, and vacuum constants μ₀ and ε₀.', [
    S('Write the two curl laws in vacuum', 'Faraday’s law couples electric circulation to changing magnetic field. The Maxwell–Ampère law couples magnetic circulation to changing electric field.', '∇×𝐄 = −∂𝐁/∂t;  ∇×𝐁 = μ₀ε₀ ∂𝐄/∂t', ('Why is the electric-field derivative present?', 'displacement-current')),
    S('Take the curl once more', 'Apply curl to Faraday’s law and interchange spatial and time differentiation. Substitute the other curl equation.', '∇×(∇×𝐄) = −μ₀ε₀ ∂²𝐄/∂t²'),
    S('Use a vector identity and zero charge', 'The identity curl curl 𝐄 = grad div 𝐄 − ∇²𝐄 simplifies because Gauss’s law in this vacuum region gives div 𝐄 = 0.', '−∇²𝐄 = −μ₀ε₀ ∂²𝐄/∂t²'),
    S('Compare coefficients with a wave equation', 'A wave of speed v satisfies ∇²𝐄 = (1/v²)∂²𝐄/∂t². Matching the coefficient predicts the propagation speed. The magnetic field obeys the same wave equation.', '1/c² = μ₀ε₀ ⇒ c = 1/√(μ₀ε₀)'),
  ], 'The vacuum wave speed is c = 299792458 m/s. A plane solution has mutually perpendicular 𝐄, 𝐁 and propagation directions.',
  'This source-free derivation does not say electromagnetic waves require a material medium. Matter changes the constitutive relations and propagation behaviour.', ('Maxwell’s Equations',))

T(33, 'em-intensity', 'Derive electromagnetic-wave intensity', '⟨S⟩ = ½ε₀cEmax² = cBmax²/(2μ₀)',
  'The Poynting vector describes electromagnetic energy flux. For a sinusoidal plane wave, averaging its squared field over a cycle gives the factor one half.',
  '𝐒: instantaneous energy flux (W/m²); Emax, Bmax: peak field magnitudes; ⟨S⟩: time-average intensity.',
  'Sinusoidal travelling plane wave in vacuum, with electric and magnetic fields in phase and perpendicular.', [
    S('Relate the wave fields', 'For a vacuum travelling wave the Maxwell curl laws require E = cB for the amplitudes and instantaneous co-phased values.', 'Emax = cBmax', ('How do Maxwell’s equations produce a travelling wave?', 'em-wave-equation')),
    S('Use electromagnetic energy flow', 'The field energy balance identifies the Poynting vector. For perpendicular plane-wave fields, its magnitude is EB/μ₀.', '𝐒 = (1/μ₀)𝐄 × 𝐁;  S = E²/(μ₀c)'),
    S('Rewrite the constants', 'Since μ₀ε₀c² = 1, the instantaneous flux becomes ε₀cE². A sinusoidal field gives E² = Emax² cos²(phase).', 'S = ε₀cEmax² cos²(phase)'),
    S('Average a full cycle', 'The mean of cos² over one period is 1/2. RMS field is Emax/√2, so the same average can be written without an extra half using Erms.', '⟨S⟩ = ½ε₀cEmax² = ε₀cErms²'),
  ], 'A vacuum plane wave with peak electric field 100 V/m has average intensity about 13.3 W/m².',
  'The factor ½ belongs to peak sinusoidal amplitudes. Do not apply it a second time to RMS field values.', ('Energy Transport and the Poynting Vector',))

T(33, 'radiation-pressure', 'Derive radiation pressure from momentum transfer', 'pabsorb = I/c;  preflect = 2I/c',
  'Electromagnetic radiation transports momentum as well as energy. Pressure follows by counting how much normal momentum a surface receives per unit area and time.',
  'I: incident time-average intensity; p: radiation pressure; c: vacuum light speed; A: illuminated area.',
  'Normally incident radiation on a stationary surface in vacuum. Compare a perfect absorber with a perfect specular reflector.', [
    S('Relate radiation energy to momentum', 'A vacuum light pulse of energy ΔE carries momentum magnitude ΔE/c along its propagation direction. This follows from electromagnetic momentum or from the photon relation.', 'Δpradiation = ΔE/c', ('Why does a photon have p = E/c?', 'photons')),
    S('Find the energy arriving per time', 'By definition of intensity, area A receives energy IA dt during time dt.', 'ΔE = IA dt'),
    S('Stop the incoming momentum for absorption', 'A perfect absorber receives the entire incoming normal momentum. Divide its momentum gain by dt to obtain force, then by A to obtain pressure.', 'F = (IA dt/c)/dt = IA/c ⇒ p = I/c'),
    S('Reverse momentum for reflection', 'A reflected pulse leaves with equal momentum in the opposite normal direction. Its momentum change doubles, so the surface receives twice the absorbed-case impulse.', 'Δpsurface = 2ΔE/c ⇒ p = 2I/c'),
  ], 'At I = 1000 W/m², perfect-absorption pressure is about 3.34 μPa and perfect-reflection pressure is about 6.67 μPa.',
  'At oblique incidence the normal momentum and illuminated geometry must be included. The displayed formulas apply to normal incidence.', ('Radiation Pressure',))

T(34, 'thin-lens', 'Derive the thin-lens imaging equation', '1/f = 1/do + 1/di;  m = −di/do',
  'A thin lens brings paraxial rays from one object point to a corresponding image point. Similar triangles made by two principal rays determine image distance and magnification.',
  'f: focal length, positive for a converging lens; do: positive real-object distance; di: positive real-image distance; m: signed transverse magnification.',
  'Thin lens, paraxial rays, same refractive medium on both sides, and the real-object/real-image positive sign convention. The geometric construction below starts with a converging lens and real image.', [
    S('Use the central ray', 'A ray through the optical centre of an ideal thin lens is treated as undeviated. Its slope relates object height ho to signed image height hi.', 'hi/ho = −di/do'),
    S('Use a parallel incident ray', 'A ray arriving parallel to the axis at height ho emerges toward the far focal point. At image distance di its height is ho(1 − di/f).', 'hi/ho = 1 − di/f'),
    S('Make both rays meet at the same image', 'Set the two height ratios equal and rearrange. This eliminates the arbitrary object height.', '−di/do = 1 − di/f ⇒ 1/f = 1/do + 1/di'),
    S('Interpret signed image distance', 'For an object inside a converging lens’s focal length, the algebra gives negative di: outgoing rays diverge and their backward extensions meet on the object side. The same signed equation describes a virtual image.'),
  ], 'A converging lens with f = 10 cm and object at do = 30 cm forms an image at di = 15 cm. Magnification is −0.50, so the image is inverted and half size.',
  'The sign convention is part of the formula. Real lenses with large apertures or thick geometry require corrections.', ('Thin Lenses',))

T(34, 'spherical-mirror', 'Derive the paraxial spherical-mirror equation', 'f = R/2;  1/f = 1/do + 1/di',
  'A spherical mirror approximately focuses rays close to its axis. The factor one half comes from the law of reflection, which doubles the small angular deflection relative to the normal.',
  'R: signed curvature radius; f: signed focal length; do, di: real-object/real-image positive distances. A concave mirror has positive R and f here.',
  'Paraxial reflection at a spherical mirror, small ray heights compared with |R|, and a consistent mirror sign convention.', [
    S('Relate surface normal to curvature', 'At height h near the axis, the surface normal points toward the centre of curvature. Its small angle to the axis is approximately h/R.', 'α ≈ h/R'),
    S('Reflect a parallel incident ray', 'The law of reflection gives equal incident and reflected angles about the normal, so the reflected ray turns through approximately 2α relative to the reversed axial direction.', 'h/f ≈ 2α ≈ 2h/R ⇒ f ≈ R/2'),
    S('Allow a finite-distance object', 'For a paraxial ray at height h, the small object-side and image-side angles are approximately h/do and h/di. The reflection geometry makes their sum 2α.', 'h/do + h/di ≈ 2h/R'),
    S('Cancel ray height', 'Divide by h and replace 2/R by 1/f. The resulting mirror equation predicts real and virtual images using signed distances.', '1/do + 1/di = 2/R = 1/f'),
  ], 'A concave mirror with R = 40 cm has f = 20 cm. An object at 60 cm forms a real image at 30 cm.',
  'A spherical mirror does not focus all parallel rays at exactly one point. The R/2 focal relation is paraxial; large ray heights produce spherical aberration.', ('Spherical Mirrors',))

T(35, 'double-slit', 'Derive the double-slit interference pattern', 'd sin θ = mλ;  I = 4I₁ cos²(πd sin θ/λ)',
  'Interference depends on relative phase. The extra travel distance from two coherent slits creates a phase difference; adding their fields gives bright and dark directions.',
  'd: slit separation; λ: wavelength in the propagation medium; I₁: intensity from either identical slit alone; m: integer order.',
  'Two coherent equal-amplitude narrow slits, common polarization, far-field observation, and negligible individual-slit diffraction variation for the displayed interference-only intensity.', [
    S('Find the path difference', 'Far from the slit pair, rays toward one observation angle are approximately parallel. The projection of the slit separation onto that direction gives the extra path.', 'Δℓ = d sin θ'),
    S('Convert distance to phase', 'Each wavelength corresponds to a phase advance of 2π. Therefore a path difference Δℓ produces phase difference δ = 2πΔℓ/λ.', 'δ = 2πd sin θ/λ'),
    S('Add wave amplitudes before squaring', 'The sum of two equal sinusoidal fields has amplitude 2E₁ cos(δ/2). Intensity is proportional to the squared amplitude.', 'I = 4I₁ cos²(δ/2)'),
    S('Identify maxima and screen spacing', 'Bright fringes require δ = 2πm. For a distant screen at distance D and small angles, y ≈ Dθ and sin θ ≈ θ.', 'd sin θ = mλ;  ym ≈ mλD/d', ('What happens when the slit width cannot be neglected?', 'single-slit')),
  ], 'For λ = 500 nm, D = 2.0 m, and d = 0.50 mm, adjacent small-angle bright fringes are separated by 2.0 mm.',
  'Add electric fields, not intensities, for coherent light. Mutually incoherent sources average away the interference cross term.', ('Young’s Interference Experiment',))

T(35, 'thin-film', 'Derive thin-film interference conditions', 'δ = (2π/λ₀)(2nt cos θt) + Δφreflection',
  'Two reflected rays can differ in both optical travel distance and reflection phase. Accounting for both effects prevents swapping the bright and dark conditions.',
  't: film thickness; n: film refractive index; θt: angle within the film; λ₀: vacuum wavelength; Δφreflection: relative reflection phase.',
  'Coherent thin film with plane parallel boundaries. The simple bright/dark examples use normal incidence, negligible absorption, and exactly one reflection phase reversal.', [
    S('Count optical path difference', 'After comparing outgoing rays at a common wavefront, the ray visiting the lower boundary has extra optical path 2nt cos θt.', 'Δoptical = 2nt cos θt'),
    S('Include reflection phase', 'At an ordinary nonabsorbing dielectric boundary, reflection from lower to higher refractive index reverses the electric-field phase by π; higher to lower does not. Compare the two reflected rays.', 'δ = 2πΔoptical/λ₀ + Δφreflection'),
    S('Apply constructive and destructive phase rules', 'Constructive interference requires total phase difference an integer multiple of 2π. With exactly one π reflection shift at normal incidence, the reflected bright condition uses a half-integer optical path.', 'bright: 2nt = (m + ½)λ₀;  dark: 2nt = mλ₀'),
    S('Check whether the shift count changes', 'If both reflected rays undergo the same phase shift, their relative reflection phase is zero. Then the bright and dark thickness conditions interchange.', 'Δφreflection = 0 ⇒ reflected bright: 2nt = mλ₀'),
  ], 'For an air–film–air layer with n = 1.5, the smallest nonzero reflected bright thickness at λ₀ = 600 nm is λ₀/(4n) = 100 nm.',
  'Do not assign the half-wavelength correction without inspecting both interfaces. Destructive cancellation also depends on matching amplitudes.', ('Interference from Thin Films',))

T(36, 'single-slit', 'Derive the single-slit diffraction envelope', 'I(θ) = I(0)(sin β/β)²;  β = πa sin θ/λ',
  'Different parts of a single slit emit coherent contributions with different travel phases. Their continuous amplitude sum produces a sinc-shaped diffraction envelope.',
  'a: slit width; λ: wavelength; θ: observation angle; β: half of the edge-to-edge phase difference.',
  'Uniformly illuminated narrow slit, scalar diffraction, coherent light, and far-field (Fraunhofer) observation.', [
    S('Assign phase across the aperture', 'An element at transverse coordinate y has path difference y sin θ relative to the centre. Its phase factor is exp(iky sin θ), with k = 2π/λ.'),
    S('Add all slit-element amplitudes', 'Uniform illumination gives equal amplitude per width element. Integrate from −a/2 to +a/2 and normalize by the zero-angle amplitude.', 'E(θ)/E(0) = (1/a) ∫[−a/2,a/2] exp(i k y sin θ) dy = sin β/β', ('Why must small contributions be integrated?', 'integrals')),
    S('Square amplitude to obtain intensity', 'Intensity is proportional to squared field magnitude. At β = 0 the limiting ratio sin β/β is one, not undefined in the physical result.', 'I(θ)/I(0) = (sin β/β)²'),
    S('Locate noncentral minima', 'The numerator vanishes at β = mπ for nonzero integer m. A narrow slit spreads the first minimum farther from the axis.', 'a sin θ = mλ,  m = ±1, ±2, …'),
  ], 'With a = 0.10 mm and λ = 500 nm, the first minimum is at θ ≈ 0.005 rad. On a screen 2 m away it lies about 10 mm from the centre.',
  'The centre m = 0 is the principal maximum, not a dark fringe. Finite-width double slits show interference fringes inside this envelope.', ('Diffraction by a Single Slit',))

T(36, 'diffraction-grating', 'Derive grating maxima and resolving power', 'd sin θ = mλ;  resolving power λ/Δλ ≈ mN',
  'Many equally spaced slits produce narrow principal maxima. Their narrowing as more slits are illuminated explains why a grating can resolve nearby wavelengths.',
  'd: slit spacing; N: illuminated slit count; m: positive diffraction order for resolving power; Δλ: small wavelength separation.',
  'Uniform coherent illumination, identical slits, far-field observation, normally incident light, and Rayleigh’s resolution criterion.', [
    S('Sum phase-shifted slit fields', 'Adjacent slits differ in phase by δ = 2πd sin θ/λ. The geometric series of N amplitudes has magnitude proportional to sin(Nδ/2)/sin(δ/2).', 'I ∝ [sin(Nδ/2)/sin(δ/2)]²'),
    S('Locate principal maxima', 'When δ = 2πm all slit contributions align. The limiting amplitude is N times one slit’s amplitude.', 'd sin θm = mλ', ('Derive the two-slit phase relation first', 'double-slit')),
    S('Estimate the first minimum near a maximum', 'Changing phase away from 2πm by approximately 2π/N makes the numerator vanish. Thus the angular half-width is λ/(Nd cos θm).', 'δθminimum ≈ λ/(Nd cos θm)'),
    S('Compare two nearby wavelengths', 'Differentiate the principal-maximum condition at fixed order: d cos θ Δθ = mΔλ. Equating that separation to the first-minimum width gives the resolution threshold.', 'mΔλ/(d cos θ) ≈ λ/(Nd cos θ) ⇒ λ/Δλ ≈ mN'),
  ], 'With N = 5000 illuminated slits at second order, ideal resolving power is 10000. Near 500 nm, the nominal resolution is about 0.05 nm.',
  'A grating must actually support the chosen order: |mλ/d| ≤ 1. Real resolution also depends on slit illumination and instrument optics.', ('Diffraction Gratings',))

T(37, 'time-dilation', 'Derive time dilation with a light clock', 'Δt = γΔτ;  γ = 1/√(1 − v²/c²)',
  'A light clock measures time by a pulse bouncing between mirrors. In a frame where the clock moves sideways, the light travels a longer diagonal path while retaining speed c.',
  'Δτ: proper time between ticks at the same clock location in its rest frame; Δt: corresponding time in a frame where the clock moves at speed v.',
  'Special relativity, inertial relative motion, vacuum light speed invariant in every inertial frame, and transverse mirror separation ℓ.', [
    S('Measure one round trip in the clock frame', 'The pulse goes a distance ℓ to the upper mirror and ℓ back. The clock remains at a fixed spatial location in this frame.', 'Δτ = 2ℓ/c'),
    S('Draw half the moving-frame trip', 'During half the interval, the clock moves horizontally vΔt/2 while the pulse moves diagonally cΔt/2. The transverse separation remains ℓ.', '(cΔt/2)² = ℓ² + (vΔt/2)²'),
    S('Solve the geometric equation', 'Move the horizontal-motion term to the left and substitute ℓ = cΔτ/2. The ratio produces the Lorentz factor.', '(c² − v²)Δt² = c²Δτ² ⇒ Δt = γΔτ'),
    S('Identify which interval is proper time', 'The proper-time events occur at one location in the clock’s rest frame. For a clock moving uniformly between those events, the other frame assigns the longer coordinate interval.', 'v = 0 ⇒ γ = 1;  0 < v < c ⇒ γ > 1'),
  ], 'At v = 0.80c, γ = 5/3. A 3 μs proper-time interval corresponds to 5 μs in the frame where the clock moves at that speed.',
  'The two observers’ statements about distant clock readings require relativity of simultaneity. Do not compare arbitrary event pairs using a proper-time label.', ('Time Dilation',))

T(37, 'relativistic-energy', 'Derive the relativistic energy–momentum relation', 'E² = p²c² + m²c⁴;  K = (γ − 1)mc²',
  'Relativistic momentum and total energy share the Lorentz factor. Eliminating speed between them yields an invariant relation that also accommodates massless particles.',
  'm: invariant mass; E: total energy; p: momentum magnitude; γ: Lorentz factor; K: kinetic energy.',
  'Special relativity for a free particle. For a massive particle use p = γmv and E = γmc², the relativistic energy–momentum definitions.', [
    S('State the relativistic quantities', 'The four-momentum has time component E/c and spatial component 𝐩. For a massive particle these are related to its four-velocity by its invariant mass.', 'E = γmc²;  p = γmv'),
    S('Subtract the squared terms', 'Factor γ²m²c⁴ out of E² − p²c². The remaining factor is 1 − v²/c².', 'E² − p²c² = γ²m²c⁴(1 − v²/c²)'),
    S('Cancel the Lorentz factor', 'By definition γ²(1 − v²/c²) = 1. This gives the invariant relation and the rest energy at p = 0.', 'E² − p²c² = m²c⁴;  Erest = mc²'),
    S('Recover the classical limit', 'K is total energy minus rest energy. For v much smaller than c, expand γ ≈ 1 + v²/(2c²), giving the familiar leading term.', 'K = (γ − 1)mc² ≈ ½mv²', ('How does classical work lead to ½mv²?', 'work-energy')),
    S('Take the massless case correctly', 'A massless particle cannot be assigned a rest frame or evaluated by inserting m = 0 into γmv at v = c. The invariant relation instead gives E = pc.', 'm = 0 ⇒ E = pc'),
  ], 'A particle at v = 0.60c has γ = 1.25, so its kinetic energy is 0.25mc² and its total energy is 1.25mc².',
  'E = mc² is rest energy for a massive particle. Its moving total energy is γmc².', ('A New Look at Energy', 'A New Look at Momentum'))

T(38, 'photons', 'Photon energy, momentum and the photoelectric effect', 'E = hf;  p = h/λ;  Kmax = hf − φ',
  'The quantum relation E = hf is a physical postulate supported by experiment. Combining it with relativistic photon momentum and energy conservation predicts the photoelectric threshold.',
  'h: Planck constant; f: light frequency; λ: vacuum wavelength; φ: material work function; Kmax: maximum emitted-electron kinetic energy.',
  'Single-photon photoemission from a surface with a specified work function, negligible multiphoton effects, and light propagation in vacuum for p = h/λ.', [
    S('State the photon energy relation', 'A photon of frequency f carries energy hf. This quantization is additional physical input and does not follow from classical wave interference alone.', 'Ephoton = hf'),
    S('Use the massless momentum relation', 'Special relativity gives E = pc for a massless particle. With c = fλ, the photon momentum magnitude is h/λ.', 'p = E/c = hf/c = h/λ', ('Why does massless energy equal pc?', 'relativistic-energy')),
    S('Balance photoemission energy', 'A photon transfers its energy to an electron. The minimum energy cost φ liberates it; electrons escaping with no additional losses have the largest kinetic energy.', 'hf = φ + Kmax'),
    S('Find threshold and stopping potential', 'Emission by this mechanism needs hf ≥ φ. A retarding potential Vs that just stops the fastest electrons satisfies eVs = Kmax.', 'fthreshold = φ/h;  eVs = hf − φ'),
  ], 'Light at 400 nm has photon energy about 3.10 eV. For a work function 2.00 eV, the maximum electron kinetic energy is about 1.10 eV.',
  'Increasing intensity at fixed frequency mainly increases photon count. Below threshold, ordinary single-photon emission does not begin merely because intensity rises.', ('Light Quanta—Photons', 'The Photoelectric Effect'))

T(38, 'compton', 'Derive the Compton wavelength shift', 'λ′ − λ = (h/(mec))(1 − cos θ)',
  'A photon scattered by a free electron exchanges both energy and momentum with it. Eliminating the electron recoil from those conservation equations gives a wavelength shift dependent on scattering angle.',
  'λ, λ′: initial and final photon wavelengths; θ: photon scattering angle; me: electron rest mass; E, E′: photon energies.',
  'Initially stationary free electron, one photon scattering event, relativistic conservation of energy and momentum. Bound-electron effects are neglected.', [
    S('Conserve total energy', 'The electron initially has rest energy mec². Its final total energy Ee is whatever remains after the photon loses energy.', 'Ee = mec² + E − E′'),
    S('Conserve vector momentum', 'The recoil electron carries the difference between initial and scattered photon momenta. Squaring the vector triangle introduces the photon scattering angle.', 'pe²c² = E² + E′² − 2EE′cos θ'),
    S('Use the electron invariant relation', 'Substitute Ee into Ee² = pe²c² + me²c⁴. Expand and cancel the common E², E′² and me²c⁴ terms.', 'mec²(E − E′) = EE′(1 − cos θ)', ('Derive the energy–momentum invariant', 'relativistic-energy')),
    S('Convert energies into wavelengths', 'Divide by EE′, then substitute 1/E = λ/(hc). The final minus initial wavelength is proportional to 1 − cos θ.', '1/E′ − 1/E = (1 − cos θ)/(mec²)'),
  ], 'At θ = 90°, the shift equals the electron Compton wavelength h/(mec) ≈ 2.43 pm. At backscattering it is twice that value.',
  'The electron recoil must be treated relativistically for the general result. The photon loses energy as its wavelength increases.', ('The Compton Effect',))

T(39, 'particle-in-box', 'Derive the energy levels of a particle in a box', 'En = n²π²ℏ²/(2mL²) = n²h²/(8mL²)',
  'Confinement imposes boundary conditions on a matter wave. Only discrete wave patterns fit a box with infinitely high walls, and each pattern has a definite allowed energy.',
  'L: one-dimensional box width; m: particle mass; n = 1, 2, …: mode number; ℏ = h/(2π).',
  'Nonrelativistic particle, infinite potential outside 0 < x < L, zero potential inside, and stationary quantum states.', [
    S('Write the Schrödinger equation inside', 'With U = 0, the stationary equation is a second-order oscillatory equation. Its general solution is a sine plus a cosine.', '−(ℏ²/(2m))ψ″ = Eψ;  ψ = A sin kx + B cos kx'),
    S('Apply the left boundary', 'The infinite-wall model requires ψ(0) = 0, so the cosine coefficient B vanishes.', 'ψ(0) = 0 ⇒ B = 0'),
    S('Apply the right boundary', 'A nonzero state must also have ψ(L) = 0. This permits only kL = nπ. The value n = 0 gives the identically zero function, which cannot be normalized.', 'kn = nπ/L'),
    S('Convert wavenumber into energy', 'Substitution into the differential equation gives E = ℏ²k²/(2m). Normalization fixes A = √(2/L).', 'En = n²π²ℏ²/(2mL²);  ψn = √(2/L)sin(nπx/L)', ('How do boundary conditions select wavelengths?', 'standing-waves')),
  ], 'An electron in a 1 nm infinite box has ground-state energy about 0.376 eV. Halving the box width raises all levels by a factor of four.',
  'The nonzero lowest energy is not thermal motion. It follows from confinement and the allowed wave states.', ('Electron in an Infinite Potential Well',))

T(39, 'tunneling', 'Why tunnelling probability decays exponentially', 'κ = √(2m(U₀ − E))/ℏ;  T ∝ e⁻²κa  (thick barrier)',
  'Where a particle’s energy lies below the potential, the stationary matter wave is exponential rather than sinusoidal. Matching it through a finite barrier leaves a transmitted wave.',
  'U₀: rectangular barrier height; E < U₀: incoming energy; a: barrier width; κ: decay constant; T: transmission probability.',
  'One-dimensional stationary nonrelativistic scattering by a rectangular barrier, with the same constant potential on the two exterior sides. The exponential scaling is the thick-barrier limit.', [
    S('Use the Schrödinger equation inside the barrier', 'Rearrange the stationary equation with U = U₀. Because U₀ − E is positive, the second derivative has the same sign as ψ.', 'ψ″ = [2m(U₀ − E)/ℏ²]ψ = κ²ψ'),
    S('Solve the constant-coefficient equation', 'Functions e±κx have second derivative κ² times themselves. Both terms are needed inside a finite barrier when matching boundaries.', 'ψbarrier = A eκx + B e⁻κx'),
    S('Match both boundaries', 'Continuity of ψ and ψ′ for a finite step relates incoming, reflected, internal and transmitted waves. This matching produces a nonzero transmitted amplitude.', 'T = [1 + U₀² sinh²(κa)/(4E(U₀ − E))]⁻¹'),
    S('Extract the thick-barrier limit', 'For κa much greater than one, sinh²(κa) ≈ e²κa/4. The dominant width dependence is therefore e⁻²κa; the squared exponent comes from probability rather than amplitude.', 'T ≈ [16E(U₀ − E)/U₀²]e⁻²κa'),
  ], 'For an electron 1 eV below the top of a barrier, κ is about 5.12 nm⁻¹. Increasing width by 0.10 nm multiplies thick-barrier transmission by about e⁻¹·⁰²⁴ ≈ 0.36.',
  'T = e⁻²κa alone omits the matching prefactor. Tunnelling does not mean the particle acquires enough classical energy to cross the barrier.', ('Tunneling',))

T(40, 'hydrogen', 'Derive hydrogen’s energy scale with the Bohr model', 'En = −mee⁴/(8ε₀²h²n²) ≈ −13.6 eV/n²',
  'The Bohr model combines Coulomb attraction with a quantization rule. It reproduces the main nonrelativistic hydrogen energy levels, while a full quantum treatment replaces its literal circular orbits.',
  'me: electron mass in the fixed-proton approximation; n: positive integer; ke = 1/(4πε₀); r: model orbit radius.',
  'One electron and a fixed proton, nonrelativistic motion, Bohr angular-momentum postulate. Reduced mass and finer corrections are neglected.', [
    S('Supply the centripetal force', 'Coulomb attraction maintains a model circular orbit. This classical relation connects speed and radius.', 'mev²/r = kee²/r²'),
    S('Add the quantization postulate', 'Bohr’s new input is angular momentum equal to nℏ. It is not implied by the force balance.', 'mevr = nℏ'),
    S('Eliminate speed', 'Substitute v = nℏ/(mer) into the force balance and solve for allowed radii.', 'rn = n²ℏ²/(mekee²)'),
    S('Add kinetic and electric potential energy', 'The force balance gives K = kee²/(2r), while potential with zero at infinity is −kee²/r. Their sum is negative and proportional to −1/r.', 'En = −kee²/(2rn) = −me(kee²)²/(2n²ℏ²)', ('Why is the electric potential energy negative?', 'electric-energy')),
  ], 'The n = 2 level is about −3.40 eV. A transition from n = 2 to n = 1 emits about 10.2 eV, corresponding to wavelength near 122 nm.',
  'This is a model derivation with an explicit quantization postulate. It does not establish that electrons follow definite classical orbits.', ('The Energies of the Hydrogen Atom',))

T(40, 'atomic-transitions', 'From atomic levels to spectral lines', 'hf = Ei − Ef;  1/λ = RH(1/nf² − 1/ni²)',
  'An atom emits or absorbs light when its internal state changes. Energy conservation gives the photon frequency once the allowed atomic energies are known.',
  'Ei, Ef: initial and final atomic energies; ni > nf: hydrogen emission levels; RH: hydrogen Rydberg constant including the appropriate mass convention.',
  'Single-photon hydrogen transitions, negligible atomic recoil for the simple formula, and the leading 1/n² energy-level approximation.', [
    S('Start with quantized energy levels', 'Write hydrogen levels as En = −A/n², where A is the positive ground-state binding-energy scale.', 'En = −A/n²', ('Where does the hydrogen energy scale come from?', 'hydrogen')),
    S('Conserve energy in emission', 'The initial atom has greater energy than the final atom. Their positive difference becomes photon energy, apart from the small recoil correction.', 'Ephoton = Ei − Ef = A(1/nf² − 1/ni²)'),
    S('Use the quantum light relation', 'Photon energy is hf = hc/λ. Dividing the level difference by hc gives the reciprocal-wavelength form.', '1/λ = [A/(hc)](1/nf² − 1/ni²)'),
    S('Distinguish energy matching from transition probability', 'Energy conservation determines possible photon frequencies. Whether a transition is strong, weak or forbidden also depends on quantum states and interaction selection rules.'),
  ], 'For ni = 3 and nf = 2, the leading energy difference is about 1.89 eV, giving a visible wavelength close to 656 nm.',
  'The photon energy is the difference of levels, not the final binding energy alone. The simple hydrogen formula does not directly fit multielectron atoms.', ('Some Properties of Atoms',))

T(41, 'drude', 'Derive conductivity in the Drude model', 'σ = ne²τ/m;  ρ = m/(ne²τ)',
  'The Drude model balances acceleration by an electric field against randomizing collisions. Its average relaxation time determines a steady drift and therefore a conductivity.',
  'n: conduction-electron density; e: positive elementary charge; τ: momentum relaxation time; m: carrier mass in the model.',
  'Classical relaxation-time model, weak steady electric field, uniform conductor, one carrier species, and a constant mean relaxation time.', [
    S('Write an average momentum balance', 'An electron accelerates opposite the electric field. Collisions relax its mean drift velocity toward zero at rate 1/τ.', 'm d𝐯d/dt = −e𝐄 − m𝐯d/τ'),
    S('Find the steady drift', 'After transients decay, the mean acceleration is zero. Solve for the drift velocity.', '𝐯d = −(eτ/m)𝐄'),
    S('Convert drift to current density', 'The electron charge is negative, so current points along the field even though drift points opposite it.', '𝐉 = n(−e)𝐯d = (ne²τ/m)𝐄', ('Derive the relation between drift and current', 'current-drift')),
    S('Identify conductivity and resistivity', 'Compare with local Ohm’s law 𝐉 = σ𝐄, then invert the coefficient. The model makes its physical dependence explicit.', 'σ = ne²τ/m;  ρ = 1/σ'),
  ], 'With n = 8.5 × 10²⁸ m⁻³, τ = 2.5 × 10⁻¹⁴ s and m = me, the model gives conductivity near 6.0 × 10⁷ S/m.',
  'This simple model does not capture quantum band structure or all temperature effects. Effective carrier masses and scattering mechanisms can matter.', ('Metals',))

T(41, 'fermi-dirac', 'Why electrons follow the Fermi–Dirac occupation rule', 'f(E) = 1 / (exp[(E − μ)/(kBT)] + 1)',
  'The Pauli exclusion principle allows at most one electron in each specified single-particle quantum state. Combining that occupancy restriction with thermal weights gives the Fermi–Dirac function.',
  'f(E): mean occupancy of one state of energy E; μ: chemical potential; T: absolute temperature; kB: Boltzmann constant.',
  'Electrons treated as independent or effective quasiparticles in thermal and particle-exchange equilibrium; each state includes its spin label.', [
    S('List the allowed occupations', 'For a particular fermion state the occupation number can be zero or one. This restriction is a quantum postulate, not an electrostatic repulsion effect.', 'nstate = 0 or 1'),
    S('Assign equilibrium statistical weights', 'In the grand-canonical description a state with energy contribution nE and particle count n has weight exp[−n(E − μ)/(kBT)]. Thus the empty-state weight is one.', 'w₀ = 1;  w₁ = exp[−(E − μ)/(kBT)]', ('Derive the energy and particle-number weights', 'boltzmann-weights')),
    S('Normalize the two possibilities', 'The probability of being occupied is its weight divided by the sum of empty and occupied weights. Since occupancy is zero or one, this probability also equals mean occupancy.', 'f(E) = w₁/(w₀ + w₁) = 1/[exp((E − μ)/(kBT)) + 1]'),
    S('Take useful limits', 'At zero temperature, states below μ are filled and those above are empty. Far above μ at nonzero temperature, occupancy is small and approaches a Boltzmann factor.', 'E − μ ≫ kBT ⇒ f(E) ≈ exp[−(E − μ)/(kBT)]'),
  ], 'At E = μ and nonzero T, the occupation is 1/2. At E − μ = kBT ln 3, it is 1/4.',
  'Occupation probability is not density of states. Counting electrons in an energy interval requires multiplying by the available-state density and integrating.', ('The Occupancy Probability',))

T(42, 'radioactive-decay', 'Derive exponential radioactive decay and half-life', 'N(t) = N₀ exp(−λdt);  t½ = ln 2/λd',
  'A constant decay probability per nucleus per unit time makes the loss rate proportional to the number remaining. Solving that rate equation gives exponential decay.',
  'N: expected number of undecayed parent nuclei; λd: decay constant (s⁻¹); A: activity in becquerels; t½: half-life.',
  'Independent nuclei with a constant decay constant and no replenishment of the parent population. The equation gives expectation values for a stochastic process.', [
    S('Translate constant probability into a rate', 'During a short interval dt, each remaining nucleus has probability λd dt of decaying. The expected number lost is therefore λdN dt.', 'dN = −λdN dt'),
    S('Separate variables and integrate', 'Divide by N and integrate from N₀ to N. The logarithm of the remaining fraction is linear in time.', 'ln(N/N₀) = −λdt ⇒ N = N₀ exp(−λdt)'),
    S('Define activity', 'Activity is the positive expected decay rate, so it is minus the derivative of the parent count.', 'A(t) = −dN/dt = λdN(t)'),
    S('Solve for half the initial population', 'At one half-life, N/N₀ = 1/2. The logarithm gives λdt½ = ln 2. Repeated half-lives multiply the remaining fraction by another half.', 't½ = ln 2/λd;  N(nt½) = N₀/2ⁿ'),
  ], 'A sample with half-life 10 days has one eighth of its original expected parent population after 30 days. Its activity is also one eighth.',
  'Half-life does not predict when an individual nucleus will decay. Daughter activity may need a separate coupled-decay calculation.', ('Radioactive Decay',))

T(42, 'binding-energy', 'Derive nuclear binding energy from mass defect', 'B = [Zmp + Nmn − mnucleus]c²;  Q = (mi − mf)c²',
  'A bound nucleus has less rest mass than the same nucleons separated. The difference records the energy that must be supplied to separate it, or that can be released in a suitable reaction.',
  'Z: proton count; N: neutron count; B > 0: binding energy; mi, mf: total initial and final rest masses for a reaction.',
  'Consistent nuclear or atomic mass bookkeeping, all reaction products included, and relativistic total-energy conservation.', [
    S('Define the separated reference state', 'Imagine Z free protons and N free neutrons at rest infinitely far apart. Their total rest energy sets the reference.', 'Eseparated = (Zmp + Nmn)c²'),
    S('Compare with the bound nucleus', 'The nucleus at rest has energy mnucleusc². Their difference is the positive energy needed to disassemble a bound ground-state nucleus.', 'B = Eseparated − mnucleusc²'),
    S('Generalize to a nuclear reaction', 'Total energy is conserved. A decrease in total rest mass becomes kinetic energy, radiation or other allowed energy forms among the products.', 'Q = (Σminitial − Σmfinal)c²', ('Why does rest mass carry energy?', 'relativistic-energy')),
    S('Use atomic masses carefully', 'Atomic tables include electron masses. If the electron count balances in the chosen reaction bookkeeping, those masses cancel; otherwise electron terms must be included. Electron binding corrections may also matter for precision.'),
  ], 'A mass defect of 0.010 unified atomic mass units corresponds to about 9.31 MeV because 1 u·c² ≈ 931.5 MeV.',
  'Do not mix a neutral-atom mass with bare proton counts without adjusting electrons. Positive Q means energy release; negative Q requires energy input.', ('Nuclear Binding Energies',))

T(43, 'nuclear-energy', 'Calculate energy released by fission or fusion', 'Q = (Σmreactants − Σmproducts)c²;  Etotal = NreactionsQ',
  'Fission and fusion release energy when the final collection of particles has lower total rest mass. Binding-energy changes provide the same accounting in a different form.',
  'Q: released energy per reaction; Nreactions: number of completed reactions; NA: Avogadro constant; Mmol: molar mass.',
  'A specified balanced reaction with all products included and consistent mass conventions. Sample totals assume the stated fraction of fuel actually reacts.', [
    S('Balance the reaction first', 'Conserve electric charge, nucleon number where applicable, and all relevant particles and quantum numbers. A mass difference has meaning only for the complete specified reaction.'),
    S('Subtract total final mass from total initial mass', 'Multiply the difference by c². Alternatively, for reactions conserving nucleons, subtract total initial binding energy from total final binding energy.', 'Q = Δmc² = Bproducts,total − Breactants,total', ('Derive binding energy from mass defect', 'binding-energy')),
    S('Count reaction events in the fuel', 'For one reacting nucleus per event, a pure sample of mass Msample contains (Msample/Mmol)NA target nuclei. Stoichiometry can require a different event count.', 'Ntargets = (Msample/Mmol)NA'),
    S('Convert units and multiply', 'Use joules per event before multiplying if power or total energy is needed. An electronvolt is e joules; a megaelectronvolt is 10⁶ times larger.', '1 MeV ≈ 1.602 × 10⁻¹³ J;  Etotal = NreactionsQ'),
  ], 'If a reaction releases 200 MeV, that is about 3.20 × 10⁻¹¹ J per event. One mole of such events releases about 1.93 × 10¹³ J.',
  'Q is not always energy deposited locally: neutrinos or escaping radiation can carry part away. Thermal-to-electric conversion adds a separate efficiency.', ('Energy from the Nucleus',))

T(43, 'chain-reaction', 'Derive the simplest chain-reaction growth law', 'Nn = N₀keffⁿ',
  'A generation model counts how many effective next-generation fission neutrons arise from each current-generation neutron. Repeated multiplication distinguishes subcritical, critical and supercritical behaviour.',
  'Nn: expected effective neutron population in generation n; keff: effective multiplication factor including losses; ℓg: idealized generation duration.',
  'A simplified discrete-generation model with constant keff and identical generation time. Real reactor dynamics also include delayed neutrons, spatial effects and feedback.', [
    S('Define the effective factor', 'Count expected neutrons that survive leakage and non-fission capture and cause the next fission generation. The ratio to the current effective population defines keff.', 'Nn₊₁ = keffNn'),
    S('Repeat the recurrence', 'Applying the same multiplier n times gives a geometric sequence.', 'N₁ = keffN₀;  N₂ = keff²N₀;  Nn = keffⁿN₀'),
    S('Classify the long-term trend', 'A factor below one makes the expected chain shrink; one maintains it on average; above one grows it in this fixed-factor model.', 'keff < 1: subcritical;  keff = 1: critical;  keff > 1: supercritical'),
    S('Relate generations to time under a strong simplification', 'If every generation takes ℓg, set n = t/ℓg. The equivalent exponential rate is ln keff divided by ℓg.', 'N(t) = N₀ exp[(ln keff)t/ℓg]'),
  ], 'With a fixed keff = 0.90, after ten generations the expected population is 0.90¹⁰ ≈ 0.349 of its starting value.',
  'This teaching model is not a reactor-control calculation. Delayed neutrons and feedback change the relation between keff and actual time behaviour.', ('The Nuclear Reactor',))

T(44, 'quark-charges', 'Build proton and neutron charge from quarks', 'qp = 2qu + qd = +e;  qn = qu + 2qd = 0',
  'The simple valence-quark model assigns two up quarks and one down quark to a proton, and one up with two down to a neutron. Adding their charges explains the observed net charges.',
  'qu = +2e/3: up-quark charge; qd = −e/3: down-quark charge; e > 0: elementary charge magnitude.',
  'Valence quantum-number accounting for ordinary nucleons. Real nucleons also contain gluons and quark–antiquark fluctuations; this is not a full microscopic mass model.', [
    S('State the constituent assignments', 'A proton has valence content uud and a neutron udd. These assignments and fractional quark charges are physical model inputs constrained by particle observations.', 'p: uud;  n: udd'),
    S('Add proton charges', 'Charge is additive. Two up-quark charges and one down-quark charge sum to one positive elementary charge.', 'qp = (2/3 + 2/3 − 1/3)e = +e'),
    S('Add neutron charges', 'One up-quark charge and two down-quark charges cancel overall. A neutral composite can therefore contain charged constituents.', 'qn = (2/3 − 1/3 − 1/3)e = 0'),
    S('Check baryon number separately', 'Each quark carries baryon number 1/3; each antiquark carries −1/3. Three valence quarks give a nucleon baryon number one. Gluons and quark–antiquark pairs add no net baryon number.', 'Bnucleon = 1/3 + 1/3 + 1/3 = 1', ('How can charge be conserved during particle changes?', 'charge-conservation')),
  ], 'Changing a down quark into an up quark raises hadron charge by e. In neutron beta decay, the emitted electron carries −e, keeping total charge balanced.',
  'Adding free quark masses does not reproduce nucleon mass. The dynamics and energy of the strong interaction are essential.', ('Leptons and Quarks',))

T(44, 'cosmological-redshift', 'Connect expansion, redshift and Hubble’s law', '1 + z = aobs/aemit;  v ≈ H₀d  (nearby galaxies)',
  'In an expanding homogeneous universe, freely propagating light stretches with the cosmic scale factor. For nearby sources the resulting small redshift is approximately proportional to distance.',
  'a(t): cosmic scale factor; z: redshift; H = ȧ/a: Hubble parameter; d: proper distance at a common cosmic time; c: vacuum light speed.',
  'Homogeneous expanding cosmological model and comoving sources for the scale-factor relation. The linear redshift–distance approximation is restricted to small z and negligible peculiar velocities.', [
    S('Define redshift from wavelengths', 'Compare a spectral line’s observed wavelength to its rest-frame emitted wavelength. Redshift is dimensionless.', 'z = (λobs − λemit)/λemit'),
    S('Supply the cosmological propagation result', 'In the homogeneous expansion model, the wavelength of a freely propagating photon scales with a(t). This is a general-relativistic model result, not a derivation from the ordinary sound Doppler formula.', 'λobs/λemit = aobs/aemit ⇒ 1 + z = aobs/aemit'),
    S('Differentiate a comoving separation', 'Two comoving locations have fixed coordinate separation χ and proper distance d = aχ at a given cosmic time. Its rate is ȧχ = Hd.', 'ḋ = ȧχ = (ȧ/a)d = Hd'),
    S('Take the nearby, short-lookback limit', 'For small redshift the expansion rate changes little while the light travels. Using lookback time about d/c gives z ≈ H₀d/c and the local Hubble relation.', 'cz ≈ H₀d  (small z)'),
  ], 'If a model uses H₀ = 70 km/s/Mpc, a nearby source at 10 Mpc has Hubble recession speed about 700 km/s and small expansion redshift about 0.0023. This is an illustrative parameter, not a claimed current measurement.',
  'At large redshift, cz is not a general recession-speed formula and distance depends on the cosmological model. Local gravitationally bound systems do not simply expand with a(t).', ('The Big Bang',))

# Shared deeper branches, reached at the exact step where they are needed.
T(2, 'integrals', 'Why an integral accumulates a rate', 'F(b) − F(a) = ∫ₐᵇ F′(t) dt',
  'A rate describes change per unit input. Multiplying a nearly constant rate by a short interval gives a small change. Adding those changes and taking a fine-interval limit gives the integral.',
  'F(t): an accumulated quantity; r(t) = F′(t): its rate; dt: infinitesimal input interval. The same mathematics applies to time, position or other variables.',
  'For this elementary construction take a continuous rate over a finite interval, so its accumulated function has the stated derivative.', [
    S('Approximate with short intervals', 'Divide [a,b] into intervals Δti. Over a short interval, rate changes little, so its contribution is approximately r(ti)Δti.', 'ΔFtotal ≈ Σi r(ti)Δti'),
    S('Take the partition limit', 'As the largest interval width approaches zero, the sum converges to the definite integral. Negative rates contribute negative changes, just as negative velocity contributes negative displacement.', '∫ₐᵇ r(t)dt = lim Σi r(ti)Δti'),
    S('Show the accumulated function has the given rate', 'Define G(t) = ∫ₐᵗ r(s)ds. Its change from t to t + h is the integral over only that short added interval. Dividing by h gives the average rate there, tending to r(t) by continuity.', 'G′(t) = lim(h → 0) [∫ₜᵗ⁺ʰ r(s)ds]/h = r(t)'),
    S('Recover the initial value', 'If F′ and G′ are equal, F − G has zero derivative and is constant. At t = a, G(a) = 0, so that constant is F(a). This proves the fundamental accumulation identity.', 'F(t) = F(a) + ∫ₐᵗ F′(s)ds'),
    S('Explain the recurring factor one half', 'For a linearly increasing rate r(t) = bt, accumulated change is the triangle area under the rate graph. An antiderivative confirms it because d(bt²/2)/dt = bt.', '∫₀ᵗ bs ds = ½bt²'),
  ], 'If velocity is v(t) = 2t m/s with t measured in seconds, displacement from 0 to 3 s is the triangular area ½ × 3 × 6 = 9 m.',
  'An indefinite integral includes an arbitrary constant. A definite integral between endpoints is a signed accumulated change, not always a positive geometric area.')

T(19, 'equipartition', 'Derive ½kBT per quadratic degree of freedom', '⟨pₓ²/(2m)⟩ = ½kBT;  ⟨Ktranslation⟩ = 3kBT/2',
  'Classical thermal equilibrium assigns Boltzmann weights to energies. A Gaussian integral, or an integration-by-parts identity, then fixes the average energy in each independent quadratic momentum term.',
  'pₓ: one momentum component; β = 1/(kBT); m: molecule mass. Statistical averages integrate all allowed momenta.',
  'Classical canonical equilibrium, separable quadratic momentum energy, unrestricted momentum range and a convergent distribution. Quantum freeze-out can invalidate classical equipartition.', [
    S('State the statistical input', 'A classical equilibrium microstate of energy H has weight proportional to exp(−βH). For an independent x momentum with energy pₓ²/(2m), its marginal weight is Gaussian.', 'w(pₓ) ∝ exp[−βpₓ²/(2m)]', ('Why do equilibrium probabilities have Boltzmann weights?', 'boltzmann-weights')),
    S('Write the normalized mean', 'The mean kinetic term is the weighted integral divided by the integral of the weight. The unknown normalization cancels.', '⟨pₓ²/(2m)⟩ = [∫ (pₓ²/(2m))e⁻ᵝᵖₓ²ᐟ⁽²ᵐ⁾ dpₓ]/[∫ e⁻ᵝᵖₓ²ᐟ⁽²ᵐ⁾ dpₓ]'),
    S('Integrate a total derivative', 'The function p exp[−βp²/(2m)] tends to zero at both infinite endpoints. Its derivative is exp[−βp²/(2m)] − (β/m)p²exp[−βp²/(2m)]. The integral of that derivative is therefore zero.', '∫ e⁻ᵝᵖ²ᐟ⁽²ᵐ⁾ dp = (β/m) ∫ p²e⁻ᵝᵖ²ᐟ⁽²ᵐ⁾ dp'),
    S('Divide to extract the mean', 'The ratio of the p² integral to the normalization integral is m/β. Multiplication by 1/(2m) gives 1/(2β) = kBT/2.', '⟨pₓ²⟩ = m/β ⇒ ⟨Kₓ⟩ = 1/(2β) = ½kBT'),
    S('Add three translational directions', 'The classical translational energy is the sum of three independent quadratic terms. Their means add.', '⟨Ktranslation⟩ = ⟨Kₓ + Kᵧ + Kz⟩ = 3kBT/2', ('Put this thermal result back into the pressure derivation', 'ideal-gas')),
  ], 'For a classical monatomic ideal gas, U = 3NkBT/2 = 3nRT/2. Thus the molar constant-volume heat capacity is CV = 3R/2.',
  'The Boltzmann distribution is an explicit statistical-mechanics input here. Molecular rotational or vibrational modes need not be classically active at every temperature.')

T(20, 'clausius', 'Why the reversible Clausius cyclic integral is zero', '∮rev δQ/T = 0',
  'A reversible engine heat ratio, the second law, and a reversible subdivision argument establish that δQrev/T has zero cyclic integral. Only after this theorem can it define a path-independent entropy difference.',
  'Qi: signed heat entering a cyclic device from reservoir i at Ti; T₀: chosen reference-reservoir temperature; Q₀: net heat absorbed from that reference reservoir.',
  'Reversible engines, positive absolute reservoir temperatures, energy conservation, the Kelvin–Planck statement of the second law, and a quasistatic limit for continuously varying temperature.', [
    S('Establish universality of reversible-engine ratios', 'Suppose two reversible engines between the same reservoirs had different efficiencies. Scale their work equally, run the more efficient forward and the other backward. Their works cancel, leaving heat transferred from cold to hot with no work. Coupling this to an ordinary engine would violate the Kelvin–Planck statement. Therefore all reversible engines between the same temperatures have the same heat ratio.'),
    S('Fix that universal ratio using one calculable engine', 'The ideal-gas Carnot construction gives |Qc|/Qh = Tc/Th without an entropy assumption. Universality then extends the ratio to every reversible engine. Equivalently, this relation defines the absolute thermodynamic temperature scale.', 'Qh/Th + Qcold,signed/Tc = 0', ('Derive the ratio using isotherms and adiabats', 'carnot')),
    S('Cancel each reservoir exchange with an auxiliary engine', 'For a reversible cyclic device absorbing signed Qi from reservoir Ti, attach a reversible auxiliary engine that absorbs −Qi from that same reservoir. The ratio theorem requires it to absorb +QiT₀/Ti from a single reference reservoir at T₀. All nonreference exchanges cancel.', 'Q₀ = T₀Σi Qi/Ti'),
    S('Apply the second law to the combined reversible cycle', 'The combined assembly exchanges heat with only the reference reservoir. If Q₀ were positive, it would turn that heat entirely into work, violating Kelvin–Planck. If Q₀ were negative, running the reversible assembly backward would do so. Therefore Q₀ = 0.', 'Σi Qi/Ti = 0'),
    S('Take the continuous reversible limit', 'Subdivide a quasistatic reversible cycle into increasingly small heat transfers, each at the instantaneous system temperature matched to its reservoir. The sum tends to the cyclic integral.', '∮rev δQ/T = 0', ('How does a sum become an integral?', 'integrals')),
    S('Define entropy only now', 'Two reversible paths between the same endpoints make a reversible closed cycle when one is reversed. The zero-integral theorem shows that their integrals agree, so the common endpoint difference can be named entropy change.', 'SB − SA ≡ ∫ₐᵇ,rev δQ/T', ('Use this result to define and calculate entropy', 'entropy')),
  ], 'For a reversible cycle exchanging +600 J at 600 K and −300 J at 300 K, the sum is 600/600 − 300/300 = 0 J/K. The net work is 300 J.',
  'Reversibility is essential to the equality. For an arbitrary cycle, Clausius’s inequality uses boundary reservoir temperatures and gives ∮δQ/T ≤ 0.')

from derivation_supplements import add_supplements
add_supplements(T, S)
