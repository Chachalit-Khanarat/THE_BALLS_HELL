import run_ball

#put your ipv4 here
useripv4 : str = ""
userport : int = 25556
st = run_ball.run(host = useripv4, port = userport)
st.run_fps_cap()