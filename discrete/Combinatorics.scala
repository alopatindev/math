object Combinatorics extends App {

  // Cartesian Product
  // n * m
  // list(itertools.product([1, 2, 3], [4, 5])) == [(1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)]
  def cartesianProduct(xs: List[List[Int]], ys: List[List[Int]]): List[List[Int]] =
    for (x <- xs; y <- ys) yield x ++ y

  // Permutations (WITHOUT Replacement), Distinct Permutations
  // (n choose k) * k! = n! / (n - k)!
  // list(itertools.permutations([1, 2, 3], 2)) == [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
  def permutations(xs: List[Int], k: Int): List[List[Int]] = {
    val n = xs.length
    val indexes = (0 until n).toList

    def generateIndexes(k: Int): List[List[Int]] =
      if (k <= 0) List(List())
      else if (k == 1) indexes.map { List(_) }
      else if (k == 2)
        for (i <- indexes; j <- indexes; if i != j)
        yield List(i, j)
      else {
        val smallerIndexes = generateIndexes(k - 1)
        for {
          i <- indexes
          group <- smallerIndexes
          if !group.contains(i)
        } yield i :: group
      }

    for {
      group <- generateIndexes(k)
      items = group.map { xs(_) }
    } yield items
  }

  // Permutations WITH Replacement
  // n^k
  // permutations_with_replacement([1, 2, 3], 2)) == [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
  def permutationsWithReplacement(xs: List[Int], k: Int): List[List[Int]] = {
    val xss = xs.map { List(_) }

    def helper(acc: List[List[Int]], k: Int): List[List[Int]] =
      if (k <= 0) List(List())
      else if (k == 1) acc
      else {
        val newAcc = cartesianProduct(acc, xss)
        helper(newAcc, k - 1)
      }

    helper(xss, k)
  }

  // Combinations (WITHOUT Replacement)
  // (n choose k)
  // list(itertools.combinations([1, 2, 3], 2)) == [(1, 2), (1, 3), (2, 3)]
  def combinations(xs: List[Int], k: Int): List[List[Int]] =
    if (k <= 0) List(List())
    else if (k == 1) xs.map { List(_) }
    else {
      def helper(xs: List[Int], acc: List[List[Int]]): List[List[Int]] = xs match {
        case x :: tail =>
          val newAcc = acc ++ combinations(tail, k - 1).map { comb => x :: comb }
          helper(tail, newAcc)
        case Nil => acc
      }
      helper(xs, List())
    }

  // Combinations WITH Replacement
  // (n + k - 1 choose k)
  // list(itertools.combinations_with_replacement([1, 2, 3], 2)) == [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
  // list(itertools.combinations_with_replacement([1, 2, 3], 3)) == [(1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 2, 2), (1, 2, 3), (1, 3, 3), (2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3)]
  def combinationsWithReplacement(xs: List[Int], k: Int): List[List[Int]] =
    if (k <= 0) List()
    else if (k == 1) xs.map { List(_) }
    else {
      def helper(xs: List[Int], acc: List[List[Int]]): List[List[Int]] = xs match {
        case x :: tail =>
          val replacement = (0 until k).map { _ => x }.toList
          val newAcc = acc ++ combinationsWithReplacement(xs, k - 1).map { comb => x :: comb }
          helper(tail, newAcc)
        case Nil => acc
      }
      helper(xs, List())
    }

  def test() {
    assert(cartesianProduct(List(List(1), List(2), List(3)), List(List(4), List(5))) == List(List(1, 4), List(1, 5), List(2, 4), List(2, 5), List(3, 4), List(3, 5)))
    assert(cartesianProduct(List(List(1), List(2), List(3)), List(List(4), List(5), List(6))) == List(List(1, 4), List(1, 5), List(1, 6), List(2, 4), List(2, 5), List(2, 6), List(3, 4), List(3, 5), List(3, 6)))

    assert(permutations(List(1, 2, 3), 0) == List(List()))
    assert(permutations(List(1, 2, 3), 1) == List(List(1), List(2), List(3)))
    assert(permutations(List(1, 2, 3), 2) == List(List(1, 2), List(1, 3), List(2, 1), List(2, 3), List(3, 1), List(3, 2)))
    assert(permutations(List(1, 2, 3), 3) == List(List(1, 2, 3), List(1, 3, 2), List(2, 1, 3), List(2, 3, 1), List(3, 1, 2), List(3, 2, 1)))

    assert(permutationsWithReplacement(List(1, 2, 3), 0) == List(List()))
    assert(permutationsWithReplacement(List(1, 2, 3), 1) == List(List(1), List(2), List(3)))
    assert(permutationsWithReplacement(List(1, 2, 3), 2) == List(List(1, 1), List(1, 2), List(1, 3), List(2, 1), List(2, 2), List(2, 3), List(3, 1), List(3, 2), List(3, 3)))
    assert(permutationsWithReplacement(List(1, 2), 3) == List(List(1, 1, 1), List(1, 1, 2), List(1, 2, 1), List(1, 2, 2), List(2, 1, 1), List(2, 1, 2), List(2, 2, 1), List(2, 2, 2)))
    assert(permutationsWithReplacement(List(1, 2, 3, 4), 2) == List(List(1, 1), List(1, 2), List(1, 3), List(1, 4), List(2, 1), List(2, 2), List(2, 3), List(2, 4), List(3, 1), List(3, 2), List(3, 3), List(3, 4), List(4, 1), List(4, 2), List(4, 3), List(4, 4)))

    assert(combinations(List(1, 2, 3), 0) == List(List()))
    assert(combinations(List(1, 2, 3), 1) == List(List(1), List(2), List(3)))
    assert(combinations(List(1, 2, 3), 2) == List(List(1, 2), List(1, 3), List(2, 3)))
    assert(combinations(List(1, 2, 3, 4), 2) == List(List(1, 2), List(1, 3), List(1, 4), List(2, 3), List(2, 4), List(3, 4)))
    assert(combinations(List(1, 2, 3), 3) == List(List(1, 2, 3)))
    assert(combinations(List(1, 2, 3, 4), 3) == List(List(1, 2, 3), List(1, 2, 4), List(1, 3, 4), List(2, 3, 4)))

    assert(permutationsWithReplacement(List(1, 2, 3), 0) == List(List()))
    assert(permutationsWithReplacement(List(1, 2, 3), 1) == List(List(1), List(2), List(3)))
    assert(combinationsWithReplacement(List(1, 2, 3), 2) == List(List(1, 1), List(1, 2), List(1, 3), List(2, 2), List(2, 3), List(3, 3)))
    assert(combinationsWithReplacement(List(1, 2, 3), 3) == List(List(1, 1, 1), List(1, 1, 2), List(1, 1, 3), List(1, 2, 2), List(1, 2, 3), List(1, 3, 3), List(2, 2, 2), List(2, 2, 3), List(2, 3, 3), List(3, 3, 3)))
    assert(combinationsWithReplacement(List(1, 2, 3, 4), 3) == List(List(1, 1, 1), List(1, 1, 2), List(1, 1, 3), List(1, 1, 4), List(1, 2, 2), List(1, 2, 3), List(1, 2, 4), List(1, 3, 3), List(1, 3, 4), List(1, 4, 4), List(2, 2, 2), List(2, 2, 3), List(2, 2, 4), List(2, 3, 3), List(2, 3, 4), List(2, 4, 4), List(3, 3, 3), List(3, 3, 4), List(3, 4, 4), List(4, 4, 4)))
  }

  test()

}
