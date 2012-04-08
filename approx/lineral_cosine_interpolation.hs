-- information: http://paulbourke.net/miscellaneous/interpolation/

xs = [10, 20, 30, 40]
ys = [10, 20, 10, 30]
smooth = 10

lineralInterpolate y0 y1 mu = y0 * (1 - mu) + y1 * mu
cosInterpolate y0 y1 mu =
    let mu' = (1 - cos(mu * pi)) / 2 in
    y0 * (1 - mu') + y1 * mu' 

mu i = i / smooth
x_dw x0 x1 smooth = (x1 - x0) / smooth

-- simple xs[i]
byIndex xs i = last (take (i + 1) xs)

-- glues lists like [[1,2,3],[4,5,6]] into [1,2,3,4,5,6]
glue [] = []
--glue xss = (head xss) ++ (glue (tail xss))
glue [[x]] = [x]
glue (x:xs) = x ++ glue xs

interpolateX xs dot_i smooth = [
    (x_dw (byIndex xs dot_i) (byIndex xs (dot_i + 1)) smooth) * i +
    (byIndex xs dot_i)
        | i <- [1 .. smooth - 1]
    ]
interpolateY ys dot_i smooth = [
    cosInterpolate (byIndex ys dot_i) (byIndex ys (dot_i + 1)) (mu (i - 1))
    --lineralInterpolate (byIndex ys dot_i) (byIndex ys (dot_i + 1)) (mu (i - 1))
        | i <- [1 .. smooth - 1]
    ]

alldots_x = glue [[byIndex xs dot_i] ++ interpolateX xs dot_i smooth | dot_i <- [0..2]] ++ [last xs]
alldots_y = glue [[byIndex ys dot_i] ++ interpolateY ys dot_i smooth | dot_i <- [0..2]] ++ [last ys]

alldots = zip alldots_x alldots_y

main = print alldots
