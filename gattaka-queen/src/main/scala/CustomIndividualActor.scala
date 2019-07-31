package ai.scynet.queen

import com.obecto.gattakka.Individual
import com.obecto.gattakka.genetics.Genome
import com.obecto.gattakka.messages.individual.Initialize
import scala.concurrent.duration._

abstract class CustomIndividualActor(genome: Genome) extends Individual(genome) {

  import context.dispatcher

  def receiveGenome(genome: Genome, data: Any) : Option[Double]

  override def customReceive = {
    case Initialize(data) =>
      val values = genome.chromosomes.head.toGene.value.asInstanceOf[Map[String, Double]]

      val x = values("x")
      val y = values("y")

      val temp1 = Math.sin(Math.sqrt(x * x + y * y))
      val temp2 = 1 + 0.001 * (x * x + y * y)
      val fitness = (0.5 + (temp1 * temp1 - 0.5) / (temp2 * temp2)).toDouble


      println(s"Point($x, $y)\n$data\n")
      val fitness1 = receiveGenome(genome, data)

      context.system.scheduler.scheduleOnce((scala.util.Random.nextInt(1000)) milliseconds) {
        dispatchFitness(fitness)
      }

  }
}
