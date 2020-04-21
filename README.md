# pendulum

Simulations of classical pendulums

# Dependencies
scipy
matplotlib
numpy
imagemagick

# Usage

To animate a simple pendulum:

```python
pendulum = Pendulum(1.0, 2.0, 120, 0)
test_system = system([pendulum])
animate_pendulum(test_system)
```

---

To animate a double pendulum:

```python
pendulum1 = Pendulum(1.0, 2.0, 120, 0)
pendulum = Double_Pendulum(pendulum1, pendulum1)
test_system = system([pendulum])
animate_pendulum(test_system)
```

---

To animate multiple pendulums in the same system:

```python
pendulum1 = Pendulum(1.0, 2.0, 120, 0)
pendulum2 = Pendulum(1.0, 3.0, 120, 0)
pendulums = [Double_Pendulum(pendulum1, pendulum1), Double_Pendulum(pendulum2, pendulum2)]
test_system = system([pendulums])
animate_pendulum(test_system)
```

---


To animate a pendulum system with a dynamic plot of their angular displacements
```python
pendulum1 = Pendulum(1.0, 2.0, 120, 0)
test_system = system([Double_Pendulum(pendulum1, pendulum1)])
animate_pend_with_graph(test_system)
```

---
